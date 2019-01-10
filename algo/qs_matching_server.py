# !/usr/bin/env python3

import grpc
import time
from concurrent import futures
import syntax_algo_pb2, syntax_algo_pb2_grpc
from qs_matching_service import ChatBotAlgoService

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = '0.0.0.0'
_PORT = '11000'

def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    servicer = ChatBotAlgoService()
    syntax_algo_pb2_grpc.add_ChatAlgoServiceServicer_to_server(
        servicer, grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    print('hello world')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)

if __name__ == '__main__':
    serve()