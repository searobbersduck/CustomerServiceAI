# !/usr/bin/env python3
# 将用户的问题，与已知选项匹配
import os
import sys
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
import fire

bc = BertClient()


choice_list_raw = ['你是谁啊','你谁啊','哪位','你是哪位','你是',
               '你是哪家公司的','你哪家公司的','你刚说的哪家公司来着',
               '你是做什么的','你做啥的','干啥的',
               '薪资大概多少','薪酬福利怎么样','哪里的工作','主要做什么','哪家公司', '你要推荐哪家公司']

choice_list = [' '.join(list(i)) for i in choice_list_raw]

# print(choice_list)

choice_arr = bc.encode(choice_list)

def get_similarity(qs):
    qs_seg = ' '.join(list(qs))
    qs_arr = bc.encode([qs_seg])
    max_score = 0
    max_i = -1
    for i in range(len(choice_list)):
        sim = cosine_similarity(choice_arr[i].reshape(-1, 768), qs_arr)
        # print('[{} | {}]\tsimilarity\t:\t{}'.format(qs, choice_list[i], sim[0][0]))
        if sim[0][0] > max_score:
            max_score = sim[0][0]
            max_i = i
    if max_score > 0.87:
        return max_score, choice_list_raw[max_i]
    else:
        return 0, 'No Matching'

def test_get_similarity(qs):
    score, res = get_similarity(qs)
    print('[{} | {}] :\t{}'.format(qs, res, score))

if __name__ == '__main__':
    fire.Fire()