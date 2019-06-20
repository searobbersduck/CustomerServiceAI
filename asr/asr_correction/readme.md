# 如何使用

1. [TensorFlow保存和恢复模型的方法总结](https://www.yueye.org/2017/summary-of-save-and-restore-models-in-tensorflow.html)
2. [【Tensorflow】报错：Cannot interpret feed_dict key as Tensor: The name 'x' refers to an operation, # > no](https://blog.csdn.net/ztf312/article/details/72859075)
3. [保存和恢复](https://www.tensorflow.org/guide/saved_model#cli_to_inspect_and_execute_savedmodel)

'''
graph = tf.Graph()

with graph.as_default():
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph('/Users/higgs/beast/code/work/CustomerServiceAI/asr/asr_correction/log/best_model-6.meta')
        saver.restore(sess, '/Users/higgs/beast/code/work/CustomerServiceAI/asr/asr_correction/log/best_model-6')
        tvs = [v for v in tf.trainable_variables()]
        for v in tvs:
            print(v.name)
            #print(sess.run(v))
        print(graph.get_tensor_by_name('lm_score:0'))
        print(graph.get_operation_by_name('inp'))
        score = graph.get_tensor_by_name('lm_score:0')
        inp = graph.get_tensor_by_name('inp:0')
        inp_len = graph.get_tensor_by_name('inp_len:0')
        score_val = sess.run(score, {inp:np_inp, inp_len:np_len})
        print(score_val)
        tf.saved_model.simple_save(sess, './3', inputs={'inp':inp, 'inp_len':inp_len}, outputs={'score':score})
        tf.train.Saver().save(sess, './sss')

'''

'''
saved_model_cli show ./3 --all
'''