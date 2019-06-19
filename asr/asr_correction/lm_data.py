# !/usr/bin/env python3
import sys
sys.path.append('./bert')
import tensorflow as tf
import lm_model
processor = lm_model.LMWikiDataProcessor()
examples = processor.get_train_examples('/Volumes/beast/data/qa/wiki/chin/extracted/AA/wiki0.txt')
print(len(examples))
# examples = examples[:20000]
max_len = 64
ds = lm_model.LMDataSet('./model/vocab.txt', max_len)
ds.file_based_convert_examples_to_features(examples, ds.tokenizer, './train.tfrecord')
# print(len(examples))