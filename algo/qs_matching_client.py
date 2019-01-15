# !/usr/bin/env python3

import grpc
import syntax_algo_pb2, syntax_algo_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = '0.0.0.0'
_PORT = '11001'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = syntax_algo_pb2_grpc.ChatAlgoServiceStub(channel=conn)
    qs = syntax_algo_pb2.QuestionText()
    while True:
        print('请输入问题：')
        qs.qs = input()
        response = client.GetQuestionType(qs)
        print("\tType: " + response.result)

if __name__ == '__main__':
    run()