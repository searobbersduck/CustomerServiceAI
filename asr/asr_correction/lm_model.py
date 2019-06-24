# !/usr/bin/env python3

import sys
sys.path.append('./bert')
import os
import tensorflow as tf
import numpy as np
import model_utils
import transformer
import embedding_layer
import tokenization
from collections import defaultdict
import collections


BASE_PARAMS = defaultdict(
    lambda: None,  # Set default value to None.

    # Input params
    default_batch_size=512,  # Maximum number of tokens per batch of examples.
    default_batch_size_tpu=32768,
    max_length=64,  # Maximum number of tokens per example.

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
    learning_rate=0.01,
    learning_rate_decay_rate=1.0,
    learning_rate_warmup_steps=16000,
    train_steps=600000,

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

class InputExample:
    def __init__(self, guid, text):
        self.guid = guid
        self.text = text

class DataProcessor(object):
  """Base class for data converters for sequence classification data sets."""

  def get_train_examples(self, data_file):
    """Gets a collection of `InputExample`s for the train set."""
    raise NotImplementedError()

  def get_dev_examples(self, data_file):
    """Gets a collection of `InputExample`s for the dev set."""
    raise NotImplementedError()

  def get_test_examples(self, data_file):
    """Gets a collection of `InputExample`s for prediction."""
    raise NotImplementedError()

class LMDataProcessor(DataProcessor):
    def get_train_examples(self, data_file):
        return self._create_examples(data_file, 'train')

    def _create_examples(self, infile, set_type):
        examples = []
        index = 0
        with open(infile, 'r', encoding='utf8') as f:
            for line in f.readlines():
                line = line.strip()
                if line == '' or line is None:
                    continue
                text = tokenization.convert_to_unicode(line)
                guid = '{}-{}'.format(set_type, index)
                examples.append(InputExample(guid, text))
        return examples

class LMWikiDataProcessor(DataProcessor):
    def get_train_examples(self, data_file):
        return self._create_examples(data_file, 'train')
    def _create_examples(self, infile, set_type):
        examples = []
        index = 0
        with open(infile, 'r', encoding='utf8') as f:
            for line in f.readlines():
                line = line.strip()
                if line == '' or line is None:
                    continue
                ss = line.split('\t')
                for s in ss:
                    if len(s) < 3:
                        continue
                    index += 1
                    text = tokenization.convert_to_unicode(s)
                    guid = '{}-{}'.format(set_type, index)
                    examples.append(InputExample(guid, text))
        return examples

class LMDataSet:
    def __init__(self, vocab_file, max_len):
        self.vocab_file = vocab_file
        self.tokenizer = tokenization.FullTokenizer(vocab_file)
        self.max_len = max_len
        self.name_to_features = {'text': tf.FixedLenFeature([self.max_len], tf.int64), 'text_len': tf.FixedLenFeature([], tf.int64)}

    def convert_single_example(self, index, example, tokenizer):
        a = example.text
        tokens_a = tokenizer.tokenize(a)
        if len(tokens_a) > self.max_len -2:
            tokens_a = tokens_a[:self.max_len-2]
        tokens_a = ['<S>'] + tokens_a + ['<T>']
        tokens_ids = tokenizer.convert_tokens_to_ids(tokens_a)
        a_len = len(tokens_a)
        while len(tokens_ids) < self.max_len:
            tokens_ids.append(0)
        return tokens_ids, a_len

    def convert_examples_to_features(self, examples, tokenizer, output_file):
        features = []
        for index, example in enumerate(examples):
            if index % 10000 == 0:
                tf.logging.info("Writing example %d of %d" % (index, len(examples)))
            feature = self.convert_single_example(index, example, tokenizer)
            features.append(feature)
        return features

    def file_based_convert_examples_to_features(self, examples, tokenizer, output_file):
        writer = tf.python_io.TFRecordWriter(output_file)
        for index, example in enumerate(examples):
            if index % 10000 == 0:
                print("Writing example %d of %d" % (index, len(examples)))
            feature = self.convert_single_example(index, example, tokenizer)

            def create_int_feature(values):
                f = tf.train.Feature(int64_list=tf.train.Int64List(value=list(values)))
                return f
            features = collections.OrderedDict()
            features['text'] = create_int_feature(feature[0])
            features['text_len'] = create_int_feature([feature[1]])
            tf_example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(tf_example.SerializeToString())
        writer.close()

    def get_ds(self, tffile, batch_size, is_training=True, drop_remainder=False):
        def _decode_record(record, name_to_features):
            example = tf.parse_single_example(record, name_to_features)
            for name in example.keys():
                t = example[name]
                if t.dtype == tf.int64:
                    t = tf.to_int32(t)
                example[name] = t
            return example
        if not os.path.isfile(tffile):
            return None
        d = tf.data.TFRecordDataset(tffile)
        if is_training:
            d = d.repeat()
            d = d.shuffle(buffer_size=100)
        d = d.apply(tf.data.experimental.map_and_batch(
            lambda record: _decode_record(record, self.name_to_features),
            batch_size = batch_size,
            drop_remainder=drop_remainder
        ))
        return d

class LMModel:
    def __init__(self, config, max_len):
        self.config = config
        self.max_len = max_len
        self.inp = tf.placeholder(tf.int32, shape=[None, max_len], name='inp')
        self.inp_len = tf.placeholder(tf.int32, shape=[None], name='inp_len')

    def predict(self, is_training):
        self.transformer = transformer.Transformer(self.config, is_training)
        self.attention_bias = model_utils.get_decoder_self_attention_bias(self.max_len)
        encoder_outputs = self.transformer.encode(self.inp, self.attention_bias)
        logits = self.transformer.embedding_softmax_layer.linear(encoder_outputs)
        loss = model_utils.soft_cross_entropy_loss(logits, self.inp, self.config['label_smoothing'],
                                                   self.config['vocab_size'])
        weights = tf.sequence_mask(self.inp_len, self.max_len, dtype=tf.int32)
        loss = loss * tf.to_float(weights)
        loss = tf.reduce_sum(loss, axis=1)
        loss = loss / tf.to_float(self.inp_len)
        return loss

    def loss_train(self, is_training):
        loss = self.predict(is_training)
        loss = tf.reduce_mean(loss, name='lm_score_train')
        return loss

    def loss_predict(self):
        loss = self.predict(False)
        loss = tf.reduce_mean(loss, name='lm_score')
        return loss

