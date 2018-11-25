# !/usr/bin/env python3

from candidate_info_pb2 import *
from candidate_info_pb2_grpc import *

# 您好，请问是xx先生吗？
def get_intention_checkname():
    node = ChatNode()
    node.question = '您好，请问是李世民先生吗？'
    node.slot = 'name'
    keys = PathKeys()
    keys.keys.append('是')
    keys.keys.append('嗯')
    node.keys['是'].CopyFrom(keys)
    keys = PathKeys()
    keys.keys.append('不是')
    node.keys['不是'].CopyFrom(keys)
    return node

# 不好意思，打扰了，再见
def get_end_sorry():
    node = ChatNode()
    node.question = '不好意思，打扰了，再见!'
    return node

# 您好，我是猎头小杜，请问您现在讲话方便吗？
def get_initention_convenient():
    node = ChatNode()
    node.question = '您好，我是猎头小杜，请问您现在讲话方便吗？'
    keys = PathKeys()
    keys.keys.append('好')
    keys.keys.append('可以聊一下')
    keys.keys.append('方便')
    keys.keys.append('感兴趣')
    keys.keys.append('挺好的')
    keys.keys.append('有什么事')
    keys.keys.append('还好')
    keys.keys.append('还行')
    node.keys['方便'].CopyFrom(keys)
    keys = PathKeys()
    keys.keys.append('不方便')
    keys.keys.append('在工作')
    keys.keys.append('稍等一会')
    keys.keys.append('我不是很感兴趣')
    keys.keys.append('能不能等会再打')
    keys.keys.append('不是很方便')
    keys.keys.append('不怎么方便')
    keys.keys.append('不好意思')
    node.keys['不方便'].CopyFrom(keys)
    return node

# 请问你的微信号是手机号吗？
def get_intention_checkwebchat():
    node = ChatNode()
    node.question = '请问你的微信号是手机号吗？'
    node.slot = 'wechat'
    keys = PathKeys()
    keys.keys.append('是')
    keys.keys.append('嗯')
    node.keys['是'].CopyFrom(keys)
    keys = PathKeys()
    keys.keys.append('不是')
    node.keys['不是'].CopyFrom(keys)
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

# 好的，我这边有好的机会会立刻联系您，祝您工作愉快，拜拜！
def get_end_happy():
    node = ChatNode()
    node.question = '好的，我这边有好的机会会立刻联系您，祝您工作愉快，拜拜！'
    return node


# 继续聊
def get_intention_next():
    node = ChatNode()
    node.question = '继续聊!'
    return node

# 请问您现在考虑新的工作机会吗？
def get_intention_searching():
    node = ChatNode()
    node.question = '请问您现在考虑新的工作机会吗？'
    node.slot = 'searching'
    keys = PathKeys()
    keys.keys.append('是')
    keys.keys.append('嗯')
    keys.keys.append('考虑')
    node.keys['是'].CopyFrom(keys)
    keys = PathKeys()
    keys.keys.append('不是')
    keys.keys.append('不考虑')
    node.keys['不是'].CopyFrom(keys)
    return node


# 我想留下您的微信号，您的微信号是手机号吗？

# 那我将我的微信号发到您的邮箱，您方便的时候可以添加下我


# 请问您目前的薪资是多少？
def get_current_salary():
    node = ChatNode()
    node.question = '请问您目前的薪资是多少？'
    node.is_record = True
    node.slot = 'current_salary'
    return node

# 请问您期望的薪资是多少？
def get_expect_salary():
    node = ChatNode()
    node.question = '请问您期望的薪资是多少？'
    node.is_record = True
    node.slot = 'expect_salary'
    return node

# 那能简单描述下，您期望什么样的行业或公司吗？
def get_expect_industry():
    node = ChatNode()
    node.question = '那能简单描述下，您期望什么样的行业或公司吗？'
    node.is_record = True
    node.slot = 'expect_industry'
    return node


def build_intention_tree():
    node_end_sorry = get_end_sorry()
    node_end_webchat = get_end_webchat()
    node_end_email = get_end_email()
    node_end_happy = get_end_happy()
    node_check_name = get_intention_checkname()
    node_check_searching = get_intention_searching()

    # record expect
    node_check_current_salary = get_current_salary()
    node_check_current_salary.children['继续'].CopyFrom(node_end_happy)
    node_check_expect_salary = get_expect_salary()
    node_check_expect_salary.children['继续'].CopyFrom(node_check_current_salary)
    node_check_expect_industry = get_expect_industry()
    node_check_expect_industry.children['继续'].CopyFrom(node_check_expect_salary)
    node_check_webchat1 = get_intention_checkwebchat()
    node_check_webchat1.children['是'].CopyFrom(node_check_expect_industry)
    node_check_webchat1.children['不是'].CopyFrom(node_check_expect_industry)
    node_check_searching.children['是'].CopyFrom(node_check_webchat1)
    node_check_searching.children['不是'].CopyFrom(node_end_sorry)


    node_check_webchat = get_intention_checkwebchat()
    node_check_webchat.children['是'].CopyFrom(node_end_webchat)
    node_check_webchat.children['不是'].CopyFrom(node_end_email)

    node_check_convenient = get_initention_convenient()
    node_check_convenient.children['不方便'].CopyFrom(node_check_webchat)
    # node_check_convenient.children['方便'].CopyFrom(get_intention_next())
    node_check_convenient.children['方便'].CopyFrom(node_check_searching)

    node_check_name.children['不是'].CopyFrom(node_end_sorry)
    node_check_name.children['是'].CopyFrom(node_check_convenient)


    tree = ChatTemplate()
    tree.root.CopyFrom(node_check_name)
    return tree

def test_CloseChatTemplateResponse():
    response = CloseChatTemplateResponse()
    response.status = 10
    response.info.sess.isCandidate = 'sf'
    response.info.sess2.isCandidate = 'sssf'
    print('hello world!')

if __name__ == '__main__':
    # tree = build_intention_tree()
    test_CloseChatTemplateResponse()

