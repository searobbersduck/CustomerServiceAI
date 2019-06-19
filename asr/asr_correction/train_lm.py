import os
import sys
sys.path.append('./bert')
import lm_model
import tensorflow as tf
import tokenization
from optimization import create_optimizer
import model_transfer as mtransfer

config = lm_model.BASE_PARAMS
tokenizer = tokenization.FullTokenizer('./model/vocab.txt')
config['vocab_size'] = len(tokenizer.vocab)
config['max_length'] = 64
config['batch_size'] = 64
vocab_file = './model/vocab.txt'
train_file = './train.tfrecord'

def make_feed_dict(model, inputs):
    dicts = {
        model.inp : inputs['text'], 
        model.inp_len : inputs['text_len'] 
    }
    return dicts

def train(train_file, vocab_file, config, log_dir, pretrained=None):
    graph = tf.Graph()
    with graph.as_default():
        ds = lm_model.LMDataSet(vocab_file, config['max_length'])
        d = ds.get_ds(train_file, config['batch_size'])
        train_iterator = d.make_one_shot_iterator()
        train_inputs = train_iterator.get_next()
        model = lm_model.LMModel(config, config['max_length'])
        loss = model.loss(True)
        train_op = create_optimizer(loss, config['learning_rate'], config['train_steps'], config['learning_rate_warmup_steps'], False)
        partialSaver = None
        if pretrained:
            partialSaver = mtransfer.partial_transfer(pretrained)
        sv = tf.train.Supervisor(graph=graph, logdir=log_dir)
        with sv.managed_session(master='') as sess:
            train_steps = config['train_steps']
#             sess.run(tf.global_variables_initializer())
            if partialSaver:
                partialSaver.restore(sess, pretrained)
            for step in range(train_steps):
                if sv.should_stop():
                    break
                try:
                    inputs = sess.run(train_inputs)
                    feed_dicts = make_feed_dict(model, inputs)
                    loss_val, _ = sess.run([loss, train_op], feed_dict=feed_dicts)
                    if (step+1)%100 == 0:
                        print('====> [{}/{}]\tloss:{.3f}'.format(step, train_steps, loss_val))
                except:
                    sv.saver.save(sess, './log/final_model', global_step=(step+1))
            sess.run(tf.global_variables_initializer())

def main():
    train(train_file, vocab_file, config, './log')

if __name__ == '__main__':
    main()