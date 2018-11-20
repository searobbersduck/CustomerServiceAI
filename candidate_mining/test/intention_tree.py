# !/usr/bin/env python3

import os
import sys
import jieba
from gensim import corpora, models, similarities


class IntentionTreeNode:
    def __init__(self, qs=None, qs_id=None, slot=None):
        self.qs = qs
        self.children = {}
        self.conds = {}
        self.conds_list = []
        self.sent2cond = {}
        self.dictionary = None
        self.tfidf = None
        self.index = None
        self.qs_id = qs_id
        if slot == '' or slot is None:
            self.slot = None
        else:
            self.slot = slot
        self.slot_info = None


    def insertNode(self, cond, node):
        self.children[cond] = node

    def insertConds(self, cond, sent):
        if cond in self.conds:
            self.conds[cond].append(sent)
        else:
            self.conds[cond] = [sent]

    def genModel(self):
        if len(self.conds.keys()) == 0:
            return
        cnt = 0
        for key, vals in self.conds.items():
            for val in vals:
                self.conds_list.append(val)
                self.sent2cond[cnt] = key
                cnt += 1
        self.conds_list.append('不知道你说的啥')
        self.sent2cond[cnt] = '不知道你说的啥'
        choice_cut = []
        for i in self.conds_list:
            data1 = ''
            this_data = jieba.cut(i)
            for item in this_data:
                data1 += item + ' '
            choice_cut.append(data1)
        docs = choice_cut
        tall = [[w1 for w1 in doc.split()] for doc in docs]
        self.dictionary = corpora.Dictionary(tall)
        corpus = [self.dictionary.doc2bow(text) for text in tall]
        self.tfidf = models.TfidfModel(corpus)
        print(self.tfidf)
        num = len(self.dictionary.token2id.keys())
        self.index = similarities.SparseMatrixSimilarity(self.tfidf[corpus],
                                                    num_features=num)
        for key, val in self.children.items():
            val.genModel()

    def getNode(self, sent):
        if self.dictionary is None:
            return None
        in_data = jieba.cut(sent)
        new_doc = ''
        for d in in_data:
            new_doc += d + ' '
        new_vec = self.dictionary.doc2bow(new_doc.split())
        sim = self.index[self.tfidf[new_vec]]
        postion = sim.argsort()[-1]
        key = self.sent2cond[postion]
        if key in self.children:
            self.slot_info = key
            return self.children[key]
        return None

    def isLeafNode(self):
        return len(self.conds.keys()) == 0

class IntentionTree:
    def __init__(self):
        self.root = None

    def genModel(self):
        node = self.root
        node.genModel()

    def getNode(self, sent):
        return self.root

# 您好，请问是xx先生吗？
def get_intention_checkname():
    node = IntentionTreeNode()
    node.qs = '您好，请问是李文斌先生吗？'
    node.insertConds('是', '是')
    node.insertConds('是', '嗯')
    node.insertConds('不是', '不是')
    return node

# 不好意思，打扰了，再见
def get_end_sorry():
    node = IntentionTreeNode()
    node.qs = '不好意思，打扰了，再见!'
    return node


# 您好，我是猎头小杜，请问您现在讲话方便吗？
def get_initention_convenient():
    node = IntentionTreeNode()
    node.qs = '您好，我是猎头小杜，请问您现在讲话方便吗？'
    node.insertConds('方便', '好')
    node.insertConds('方便', '可以聊一下')
    node.insertConds('方便', '方便')
    node.insertConds('方便', '感兴趣')
    node.insertConds('方便', '挺好的')
    node.insertConds('方便', '有什么事')
    node.insertConds('方便', '还好')
    node.insertConds('方便', '还行')
    node.insertConds('不方便', '不方便')
    node.insertConds('不方便', '在工作')
    node.insertConds('不方便', '稍等一会')
    node.insertConds('不方便', '我不是很感兴趣')
    node.insertConds('不方便', '能不能等会再打')
    node.insertConds('不方便', '不是很方便')
    node.insertConds('不方便', '不怎么方便')
    node.insertConds('不方便', '不好意思')
    return node


# 请问你的微信号是手机号吗？
def get_intention_checkwebchat():
    node = IntentionTreeNode()
    node.qs = '请问你的微信号是手机号吗？'
    node.insertConds('是', '是')
    node.insertConds('是', '嗯')
    node.insertConds('不是', '不是')
    return node

# 好的，我们之后微信聊，祝您工作愉快！拜拜！
def get_end_webchat():
    node = IntentionTreeNode()
    node.qs = '好的，我们之后微信聊，祝您工作愉快！拜拜！'
    return node

# 好的，我这边有些不错的工作机会，待会发送到您的邮箱，如果有需要，可以给我打电话，也可以加微信，祝您工作愉快！拜拜！
def get_end_email():
    node = IntentionTreeNode()
    node.qs = '好的，我这边有些不错的工作机会，待会发送到您的邮箱，如果有需要，可以给我' \
              '打电话，也可以加微信，祝您工作愉快！拜拜！'
    return node


def test_IntentionTree():
    root_node = IntentionTreeNode()
    root_node.qs = '请问您现在方便吗？'
    root_node.insertNode('方便', IntentionTreeNode('继续聊！'))
    root_node.insertNode('不方便', IntentionTreeNode('不好意思，打扰了！'))
    root_node.insertConds('方便', '好')
    root_node.insertConds('方便', '可以聊一下')
    root_node.insertConds('方便', '方便')
    root_node.insertConds('方便', '感兴趣')
    root_node.insertConds('方便', '挺好的')
    root_node.insertConds('方便', '有什么事')
    root_node.insertConds('方便', '还好')
    root_node.insertConds('方便', '还行')
    root_node.insertConds('不方便', '不方便')
    root_node.insertConds('不方便', '在工作')
    root_node.insertConds('不方便', '稍等一会')
    root_node.insertConds('不方便', '我不是很感兴趣')
    root_node.insertConds('不方便', '能不能等会再打')
    root_node.insertConds('不方便', '不是很方便')
    root_node.insertConds('不方便', '不怎么方便')
    root_node.insertConds('不方便', '不好意思')
    intention_tree = IntentionTree()
    intention_tree.root = root_node
    intention_tree.genModel()
    while True:
        choice_input = input('{}\n'.format(intention_tree.root.qs))
        child_node = intention_tree.root.getNode(choice_input)
        if child_node is not None:
            print(child_node.qs)
        else:
            print('不知道你说的是啥！')
        print('\n\n')

def build_intention_tree():
    node_end_sorry = get_end_sorry()
    node_end_webchat = get_end_webchat()
    node_end_email = get_end_email()
    node_check_name = get_intention_checkname()
    node_check_name.insertNode('不是', node_end_sorry)
    node_check_convenient = get_initention_convenient()
    node_check_name.insertNode('是', node_check_convenient)
    node_check_webchat = get_intention_checkwebchat()
    node_check_convenient.insertNode('不方便', node_check_webchat)
    node_check_convenient.insertNode('方便', IntentionTreeNode('继续聊！！！'))
    node_check_webchat.insertNode('是', node_end_webchat)
    node_check_webchat.insertNode('不是', node_end_email)
    intention_tree = IntentionTree()
    intention_tree.root = node_check_name
    intention_tree.genModel()
    node = intention_tree.getNode('开始')
    while True:
        if node is not None:
            if node.isLeafNode():
                print('{}\n'.format(node.qs))
                print('====> 本次通话结束!')
                break
            choice_input = input('{}\n'.format(node.qs))
            node1 = node.getNode(choice_input)
            if node1 is not None:
                node = node1
                # print('{}\n'.format(node.qs))
            else:
                print('不知道你说的是啥！')
    print('hello world!')

def test_build_intention_tree():
    build_intention_tree()

if __name__ == '__main__':
    # test_IntentionTree()
    test_build_intention_tree()


