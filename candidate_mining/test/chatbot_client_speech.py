# !/usr/bin/env python3

import sys
sys.path.append('./')
sys.path.append('../../asr')

import grpc
import candidate_info_pb2, candidate_info_pb2_grpc
from candidate_info import *

from speech_utils import *


_HOST = 'localhost'
_PORT = '8080'

def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = candidate_info_pb2_grpc.ChatServiceStub(channel=conn)
    template_tree = build_intention_tree()
    response = client.BuildChatTemplate(template_tree)
    answer = ''
    print_one = True
    while True:
        req = QuestionRequest()
        req.answer = answer
        req.task_id = 500
        response = client.GetQuestion(req)
        machine = '{}\n'.format(response.question)
        if response.status != 2 and response.question != '':
            result = sp_client.synthesis(response.question)
            play_mp3(result)
            print(machine)
            # answer = input(machine)
            answer = ''
            result = sp_client.asr(audio_record_rt(5), 'wav', 16000, {"cuid": CUID, "dev_pid": DEV_PID, })
            if result["err_msg"] == "success.":
                # print(result["result"])
                print(result["result"])
                answer = result['result'][0]
            else:
                # print(result["err_msg"])
                # return ""
                pass
            print_one = True
        else:
            if print_one == False:
                continue
            print_one = False
            if response.question != "":
                result = sp_client.synthesis(response.question)
                play_mp3(result)
            print(response.question)
            answer=''
            req = CloseChatTemplateRequest()
            req.task_id = 200
            response = client.CloseChatTemplate(req)
            print('====> 本次会话获取信息：')
            print(response.info.info)
            print('\n')

    # response = client.GetQuestion(data_pb2.Data(text='hello,world!'))
    print("received: " + response.text)

if __name__ == '__main__':
    run()
