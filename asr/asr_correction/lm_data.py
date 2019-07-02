# !/usr/bin/env python3
import sys
sys.path.append('./bert')
import tensorflow as tf
import lm_model
from glob import glob
import os
import fire

# processor = lm_model.LMWikiDataProcessor()
# examples = processor.get_train_examples('/Volumes/beast/data/qa/wiki/chin/extracted/AA/wiki0.txt')

# processor = lm_model.LMResumeDataProcessor()
# examples = processor.get_train_examples('/Users/higgs/beast/data/lm/part-r-00000')

# print(len(examples))
# # examples = examples[:20000]
# max_len = 64
# ds = lm_model.LMDataSet('./model/vocab.txt', max_len)
# ds.file_based_convert_examples_to_features(examples, ds.tokenizer, './train.tfrecord')
# print(len(examples))

max_len = 64

def gen_resume_tfrecord(pat, outdir, out_prefix='train'):
    files = glob(pat)
    ds = lm_model.LMDataSet('./model/vocab.txt', max_len)
    for index, file in enumerate(files):
        processor = lm_model.LMResumeDataProcessor()
        examples = processor.get_train_examples(file)
        outfile = os.path.join(outdir, '{}-{}.tfrecord'.format(out_prefix, index))
        print('\n')
        print('====> begin processing {}'.format(file))
        ds.file_based_convert_examples_to_features(examples, ds.tokenizer, outfile)
        print('====> out {}'.format(outfile))
        print('====> end processing {}'.format(file))
        print('\n')


def gen_wiki_tfrecord(pat, outdir, out_prefix='train'):
    files = glob(pat)
    ds = lm_model.LMDataSet('./model/vocab.txt', max_len)
    for index, file in enumerate(files):
        processor = lm_model.LMWikiDataProcessor()
        examples = processor.get_train_examples(file)
        outfile = os.path.join(outdir, '{}-{}.tfrecord'.format(out_prefix, index))
        print('\n')
        print('====> begin processing {}'.format(file))
        ds.file_based_convert_examples_to_features(examples, ds.tokenizer, outfile)
        print('====> out {}'.format(outfile))
        print('====> end processing {}'.format(file))
        print('\n')
        
if __name__ == '__main__':
	fire.Fire()