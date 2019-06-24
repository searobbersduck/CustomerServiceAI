# !/usr/bin/env python3

import tensorflow as tf
import os
import fire

'''
usage: python lm_model_to_tfserver.py convert_tfmodel_to_tfservermodel ./log/model.ckpt-127188.meta ./log/model.ckpt-127188 4
'''

def convert_tfmodel_to_tfservermodel(meta_file, ckpt_file, version):
    graph = tf.Graph()
    with graph.as_default():
        with tf.Session() as sess:
            saver = tf.train.import_meta_graph(meta_file)
            saver.restore(sess, ckpt_file)
            tvs = [v for v in tf.trainable_variables()]
            # for v in tvs:
            #     print(v.name)
            # print(graph.get_tensor_by_name('lm_score:0'))
            # print(graph.get_operation_by_name('inp'))
            score = graph.get_tensor_by_name('lm_score:0')
            inp = graph.get_tensor_by_name('inp:0')
            inp_len = graph.get_tensor_by_name('inp_len:0')
            # score_val = sess.run(score, {inp: np_inp, inp_len: np_len})
            # print(score_val)
            tf.saved_model.simple_save(sess, './{}'.format(version), inputs={'inp': inp, 'inp_len': inp_len}, outputs={'score': score})
            # tf.train.Saver().save(sess, './sss')
            print('save tf serving model finished!')

if __name__ == '__main__':
    fire.Fire()