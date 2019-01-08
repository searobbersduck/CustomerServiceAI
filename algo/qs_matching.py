# !/usr/bin/env python3
# 将用户的问题，与已知选项匹配
import os
import sys
from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
import fire
import time

bc = BertClient()

THRESHOLD = 0.89

choice_map = {
    'WHO': ['哪位?','你是哪位?'],
    'YOUR_COMPANY':['你是哪家公司的','你哪家公司的','你刚说的哪家公司来着'],
    'YOUR_CARRER':['你是做什么的','你做啥的','干啥的'],
    'SALARY':['薪资大概多少','薪酬福利怎么样','工资多少','待遇怎么样', '钱多少'],
    'COMPANY':['哪里的工作','主要做什么','哪家公司', '你要推荐哪家公司','在哪里'],
    'WORKING_STATUS':['工作累吗？']
}

choice_list_raw = []
choice_id2tag = {-1:'NO_MATCH'}
cnt_i = 0
for key in choice_map.keys():
    tag_l = choice_map[key]
    if len(tag_l) > 0:
        for i in range(len(tag_l)):
            choice_list_raw.append(tag_l[i])
            choice_id2tag[cnt_i] = key
            cnt_i += 1

# choice_list_raw = ['你是谁啊?','你谁啊','哪位','你是哪位','你是？',
#                '你是哪家公司的','你哪家公司的','你刚说的哪家公司来着',
#                '你是做什么的','你做啥的','干啥的',
#                '薪资大概多少','薪酬福利怎么样','哪里的工作','主要做什么','哪家公司', '你要推荐哪家公司']

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
    if max_score > THRESHOLD:
        return max_score, choice_list_raw[max_i], max_i
    else:
        return 0, '不知道你说的啥', -1

def test_get_similarity(qs):
    t1 = time.time()
    score, res, index = get_similarity(qs)
    t2 = time.time()
    # print('[{} | {}] :\t{:.3f}\telapse time:\t{:.1f}ms'.format(qs, res, score, 1000*(t2-t1)))
    # print('[{} | {} | {}] :\t{:.3f}\telapse time:\t{:.1f}ms'.format(qs, res, choice_id2tag[index], score, 1000 * (t2 - t1)))
    print('[{} | {} | {}] :\t{:.3f}'.format(qs, res, choice_id2tag[index], score))


def get_industry_similarity(ind1, ind2):
    qs_seg1 = ' '.join(list(ind1))
    qs_arr1 = bc.encode([qs_seg1])
    qs_seg2 = ' '.join(list(ind2))
    qs_arr2 = bc.encode([qs_seg2])
    sim = cosine_similarity(qs_arr1, qs_arr2)
    print('[{} | {}] 相似度：{}'.format(ind1, ind2, sim[0][0]))


if __name__ == '__main__':
    fire.Fire()