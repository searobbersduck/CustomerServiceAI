#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File: summary_model.py
# Project: transformer
# Author: koth (Koth Chen)
# -----
# Last Modified: 2019-06-06 1:53:48
# Modified By: koth (nobody@verycool.com)
# -----
# Copyright 2020 - 2019

import numpy as np
import tensorflow as tf
import optimization
from transformer import Transformer, LayerNormalization
from collections import defaultdict
import model_utils


BASE_PARAMS = defaultdict(
    lambda: None,  # Set default value to None.

    # Input params
    default_batch_size=512,  # Maximum number of tokens per batch of examples.
    default_batch_size_tpu=32768,
    max_length=200,  # Maximum number of tokens per example.

    # Model params
    initializer_gain=2.0,  # Used in trainable variable initialization.
    initializer_range = 0.02,
    vocab_size=32003,  # Number of tokens defined in the vocabulary file.
    hidden_size=200,  # Model dimension in the hidden layers.
    num_hidden_layers=6,  # Number of layers in the encoder and decoder stacks.
    num_heads=8,  # Number of heads to use in multi-headed attention.
    filter_size=800,  # Inner layer dimension in the feedforward network.

    # Dropout values (only used when training)
    layer_postprocess_dropout=0.1,
    attention_dropout=0.1,
    relu_dropout=0.1,

    # Training params
    label_smoothing=0.1,
    learning_rate=2.0,
    learning_rate_decay_rate=1.0,
    learning_rate_warmup_steps=16000,

    # Optimizer params
    optimizer_adam_beta1=0.9,
    optimizer_adam_beta2=0.997,
    optimizer_adam_epsilon=1e-09,

    # Default prediction params
    extra_decode_length=90,
    beam_size=4,
    alpha=0.6,  # used to calculate length normalization initializer_rangen beam search
    
    num_types = 3, # how many id types
    # TPU specific parameters
    use_tpu=False,
    static_batch=False,
    allow_ffn_pad=True,
)

class SummaryModel:
    def __init__(self, maxLength, maxYLength):
        self.transformer_conf=BASE_PARAMS
        self.vocab_size = self.transformer_conf['vocab_size']
        self.embed_dim = self.transformer_conf['hidden_size']
        self.num_units = self.transformer_conf['hidden_size']
        self.max_length = maxLength
        self.max_y_length = maxYLength
        self.inp_X = tf.placeholder(
            tf.int32, shape=[None, self.max_length], name="inp_x")
        self.inp_Y = tf.placeholder(
            tf.int32, shape=[None, self.max_y_length], name="inp_y")
        self.max_decode_length = tf.placeholder(
            tf.int32, shape=[], name="decode_len")
        
        self.a_length = tf.placeholder(tf.int32, shape=[None], name="alength")
        self.totalLength = tf.placeholder(
            tf.int32, shape=[None], name="totalLength")
        self.target_length = tf.placeholder(
            tf.int32, shape=[None], name="y_length")
        self.END_TOKEN = self.transformer_conf['vocab_size']-2
        

    def inference(self,transformer, name=None, training=True):
        with tf.variable_scope("tf_inference"):
            X = self.inp_X
            shapeS = tf.shape(X)
            padCLS = tf.ones([shapeS[0], 1], dtype=tf.int32) * (self.vocab_size-1)
            paddedX = tf.concat([padCLS, X], axis=1)
            amask = tf.sequence_mask(
                self.a_length, self.max_length+1, dtype=tf.int32)
            abmask = tf.sequence_mask(
                self.totalLength, self.max_length+1, dtype=tf.int32)
            totalmask = amask + abmask
            results, _ = transformer(paddedX,totalmask, self.inp_Y)
            predsIds =None
            if not training:
                preds, _ = transformer(paddedX,totalmask)
                predsIds = tf.identity(
                    preds['outputs'], name='predictions')
        return results , predsIds

    def loss(self,training=True):
        transformer = Transformer(self.transformer_conf, training)
        train_outputs, pred_outputIds = self.inference(transformer,name="final_inference", training=training)
        oshape = tf.shape(train_outputs)
        targetOutputs = self.inp_Y[:, :oshape[-1]]
       
        weights = tf.sequence_mask(
                self.target_length, self.max_y_length, dtype=tf.int32)
        targetWeights = weights[:, :oshape[-1]]
        loss = model_utils.soft_cross_entropy_loss(train_outputs,targetOutputs,self.transformer_conf['label_smoothing'], self.transformer_conf['vocab_size'])
        loss = loss * tf.to_float(targetWeights)
        
        actuallyLength = tf.reduce_sum(targetWeights, axis=1)
        loss = tf.reduce_sum(loss, axis=1)
        loss = loss / tf.cast(actuallyLength, tf.float32)
        loss = tf.reduce_mean(loss)
        
        distance = None
        reference_length = None
        if not training:
            nonzero_idx = tf.where(tf.not_equal(pred_outputIds, self.END_TOKEN))
            reference_length1 = tf.shape(nonzero_idx)[0]
            sparse_outputs = tf.SparseTensor(nonzero_idx,
                                            tf.gather_nd(pred_outputIds, nonzero_idx),
                                            tf.shape(pred_outputIds, out_type=tf.int64))
            
            nonzero_idx = tf.where(tf.not_equal(targetOutputs,  self.END_TOKEN))
            label_sparse_outputs = tf.SparseTensor(nonzero_idx,
                                                tf.gather_nd(targetOutputs, nonzero_idx),
                                                tf.shape(targetOutputs, out_type=tf.int64))
            distance = tf.reduce_sum(
                tf.edit_distance(sparse_outputs, label_sparse_outputs, normalize=False))
            reference_length2 = tf.shape(nonzero_idx)[0]
            reference_length = tf.reduce_max([reference_length1,reference_length2])
        return loss, distance, reference_length, pred_outputIds
