# !/usr/bin/env python3

from grpc.beta import implementations
import numpy as np
import tensorflow as tf

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2

import sys
sys.path.append('./bert')
import tokenization
import numpy as np
import fire

'''
usage: python lm_client.py get_score '今天天气好晴朗，处处好风光' 64

'''

server = '172.16.52.70:8500'

host, port = server.split(':')
#
# channel = implementations.insecure_channel(host, int(port))
#
# stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
#
# request = predict_pb2.PredictRequest()
#
# request.model_spec.name = 'saved_model'


def get_connection(host, port, model_name):
    host, port = server.split(':')
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)
    request = predict_pb2.PredictRequest()
    request.model_spec.name = 'saved_model'
    return request, stub

def get_input_data(text_a, max_len, tokenizer):
    tokens_a = tokenizer.tokenize(text_a)
    tokens_a = ['<S>'] + tokens_a + ['<T>']
    ids_a = tokenizer.convert_tokens_to_ids(tokens_a)
    x_data = np.zeros([max_len], dtype=np.int32)
    len_max = min(max_len, len(ids_a))
    x_data[:len_max] = ids_a
    y_data = [len_max]
    return x_data, y_data

request, stub = get_connection(host, int(port), 'saved_model')

tokenizer = tokenization.FullTokenizer('./vocab.txt')

def get_score(text_a, max_len, tokenizer=tokenizer):
    x_data, y_data = get_input_data(text_a, max_len, tokenizer)
    request.inputs['inp'].CopyFrom(tf.contrib.util.make_tensor_proto(x_data, shape=[1, 64]))
    request.inputs['inp_len'].CopyFrom(tf.contrib.util.make_tensor_proto(y_data, shape=[1]))
    result = stub.Predict(request, 10.0)
    print(result)

if __name__ == '__main__':
    fire.Fire()