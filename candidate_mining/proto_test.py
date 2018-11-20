# !/usr/bin/env python3

from candidate_info_pb2_grpc import *
from candidate_info_pb2 import *

audio_map_id = {
    'get_end_sorry':10,

}

node = ChatNode()
node.question = 'asdfasdf'
node.question_id = 2

def get_end_sorry():
    node = ChatNode()
    node.question = '不好意思，打扰了，再见!'
    return node

def get_intention_checkname():
    node = ChatNode()
    node.question = '您好，请问是李文斌先生吗？'
    childnode = node.children[0]
    childnode.choice = '是'
    childnode.keys.append('是')
    childnode.keys.append('嗯')
    childnode = node.children[1]
    childnode.choice = '不是'
    childnode.keys.append('不是')
    return node

def get_initention_convenient():
    node = ChatNode()
    node.question = '您好，我是猎头小杜，请问您现在讲话方便吗？'
    childnode = node.children[0]
    childnode.choice = '方便'
    childnode.keys.append('好')
    childnode.keys.append('可以聊一下')
    childnode.keys.append('方便')
    childnode.keys.append('感兴趣')
    childnode.keys.append('挺好的')
    childnode.keys.append('有什么事')
    childnode.keys.append('还好')
    childnode.keys.append('还行')
    childnode = node.children[1]
    childnode.choice = '不方便'
    childnode.keys.append('不方便')
    childnode.keys.append('在工作')
    childnode.keys.append('稍等一会')
    childnode.keys.append('我不是很感兴趣')
    childnode.keys.append('能不能等会再打')
    childnode.keys.append('不是很方便')
    childnode.keys.append('不怎么方便')
    childnode.keys.append('不好意思')
    return node

# 请问你的微信号是手机号吗？
def get_intention_checkwebchat():
    node = ChatNode()
    node.question = '请问你的微信号是手机号吗？'
    childnode = node.children[0]
    childnode.choice = '是'
    childnode.keys.append('是')
    childnode.keys.append('嗯')
    childnode = node.children[1]
    childnode.choice = '不是'
    childnode.keys.append('不是')
    return node

# 好的，我们之后微信聊，祝您工作愉快！拜拜！
def get_end_webchat():
    node = ChatNode()
    node.question = '好的，我们之后微信聊，祝您工作愉快！拜拜！'
    return node

# 好的，我这边有些不错的工作机会，待会发送到您的邮箱，如果有需要，可以给我打电话，也可以加微信，祝您工作愉快！拜拜！
def get_end_email():
    node = ChatNode()
    node.question = '好的，我这边有些不错的工作机会，待会发送到您的邮箱，如果有需要，可以给我' \
              '打电话，也可以加微信，祝您工作愉快！拜拜！'
    return node

node = get_intention_checkname()

def build_intention_tree():
    node_end_sorry = get_end_sorry()
    node_end_webchat = get_end_webchat()
    node_end_email = get_end_email()
    node_check_name = get_intention_checkname()
    for i in range()
    node_check_name.insertNode('不是', node_end_sorry)
    print('hello world!')

build_intention_tree()

print('hello world!')