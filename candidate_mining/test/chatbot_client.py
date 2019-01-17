# !/usr/bin/env python3

import sys
sys.path.append('./')
sys.path.append('../../asr')

import grpc
import candidate_info_pb2, candidate_info_pb2_grpc
from candidate_info import *

from speech_utils import *
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_id', type=int, default=0)
    return parser.parse_args()

opts = parse_args()

_HOST = '172.16.56.183'
_HOST = '0.0.0.0'
# _HOST = '192.168.32.19'
_PORT = '10180'
# _HOST = '172.16.52.70'
# _PORT = '20801'
# _HOST = '0.0.0.0'
# _PORT = '26530'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = candidate_info_pb2_grpc.ChatServiceStub(channel=conn)
    template_tree = build_intention_tree()
    template_tree.task_id = opts.task_id
    response = client.BuildChatTemplate(template_tree)
    answer = ''
    print_one = True
    while True:
        req = QuestionRequest()
        req.answer = answer
        req.task_id = opts.task_id
        response = client.GetQuestion(req)
        machine = '{}\n'.format(response.question)
        if response.status != 2 and response.question != '':
            answer = input(machine)
            print_one = True
        else:
            if print_one == False:
                continue
            print_one = False
            print(response.question)
            answer=''
            req = CloseChatTemplateRequest()
            req.task_id = opts.task_id
            response = client.CloseChatTemplate(req)
            print('====> 本次会话获取信息：')
            print(response.info.info)
            print('\n')

    # response = client.GetQuestion(data_pb2.Data(text='hello,world!'))
    print("received: " + response.text)

if __name__ == '__main__':
    run()
