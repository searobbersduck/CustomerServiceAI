# !/usr/bin/env python3

import grpc
import candidate_info_pb2, candidate_info_pb2_grpc

_HOST = 'localhost'
_PORT = '8080'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = candidate_info_pb2_grpc.ChatServiceStub(channel=conn)
    response = client.GetQuestion(data_pb2.Data(text='hello,world!'))
    print("received: " + response.text)

if __name__ == '__main__':
    run()
