# !/usr/bin/env python3

import grpc
import time
from concurrent import futures
import syntax_algo_pb2, syntax_algo_pb2_grpc
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
import fire

THRESHOLD = 0.89

class ChatBotAlgoService(syntax_algo_pb2_grpc.ChatAlgoServiceServicer):
    def __init__(self):
        self.bc = BertClient()
        self.choice_map = {
            'WHO': ['哪位?', '你是哪位?','请问哪位？'],
            'YOUR_COMPANY': ['你是哪家公司的', '你哪家公司的', '你刚说的哪家公司来着'],
            'YOUR_CARRER': ['你是做什么的', '你做啥的', '干啥的'],
            'SALARY': ['薪资大概多少', '薪酬福利怎么样', '工资多少', '待遇怎么样', '钱多少'],
            'COMPANY': ['哪里的工作', '哪家公司', '你要推荐哪家公司', '在哪里'],
            'WORKING_STATUS': ['工作累吗？'],
            'YOUR_TARGET':['你有什么事？','有何贵干啊?'],
            'BYE':['再见','拜拜,', '拜拜'],
            'CALL_LATER':['晚点再打过来'],
        }
        self.choice_list_raw = []
        self.choice_id2tag = {-1: 'NO_MATCH'}
        cnt_i = 0
        for key in self.choice_map.keys():
            tag_l = self.choice_map[key]
            if len(tag_l) > 0:
                for i in range(len(tag_l)):
                    self.choice_list_raw.append(tag_l[i])
                    self.choice_id2tag[cnt_i] = key
                    cnt_i += 1
        self.choice_list = [' '.join(list(i)) for i in self.choice_list_raw]
        self.choice_arr = self.bc.encode(self.choice_list)
        print('start qs matching service ...')

    def get_similarity(self, qs):
        qs_seg = ' '.join(list(qs))
        qs_arr = self.bc.encode([qs_seg])
        max_score = 0
        max_i = -1
        for i in range(len(self.choice_list)):
            sim = cosine_similarity(self.choice_arr[i].reshape(-1, 768), qs_arr)
            # print('[{} | {}]\tsimilarity\t:\t{}'.format(qs, choice_list[i], sim[0][0]))
            if sim[0][0] > max_score:
                max_score = sim[0][0]
                max_i = i
        if max_score > THRESHOLD:
            return max_score, self.choice_list_raw[max_i], max_i
        else:
            return 0, '不知道你说的啥', -1

    def GetQuestionType(self, request, context):
        qs = request.qs
        score, res, index = self.get_similarity(qs)
        result = self.choice_id2tag[index]
        response = syntax_algo_pb2.QuestionResponse()
        response.result = result
        print('{}\t{}'.format(qs, result))
        return response

def test_ChatBotAlgoService():
    ser = ChatBotAlgoService()
    req = syntax_algo_pb2.QuestionText()
    req.qs = "您是哪位？"
    response = ser.GetQuestionType(req, None)
    print('{}\t{}'.format(req.qs, response.result))

if __name__ == '__main__':
    test_ChatBotAlgoService()
