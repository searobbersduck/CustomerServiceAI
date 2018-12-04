# !/usr/bin/env python3

import grpc
import time
from concurrent import futures
import candidate_info_pb2, candidate_info_pb2_grpc
from intention_tree import *
from candidate_info import *
import json

class ChatBotService(candidate_info_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.name = 'ChatBotService'
        self.node = None
        self.tree = IntentionTree()
        self.cur_node = None
        self.slot_dict = {}

    def resetSlot(self):
        self.slot_dict = {}

    def getNode(self, grpc_node):
        node = IntentionTreeNode(grpc_node.question, grpc_node.question_id,
                                 grpc_node.slot, grpc_node.is_record, grpc_node.need_answer)
        for child_name in list(grpc_node.children):
            keys_list = list(grpc_node.keys[child_name].keys)
            for key in keys_list:
                node.insertConds(child_name, key)
            if len(keys_list) == 0:
                node.insertConds(child_name, child_name)
            child_node = self.getNode(grpc_node.children[child_name])
            node.insertNode(child_name, child_node)
            print('insert node:{}\t\t{}'.format(child_name, grpc_node.children[child_name].question))
        return node

    def BuildChatTemplate(self, request, context):
        root_node = request.root
        node = self.getNode(root_node)
        self.tree.root = node
        self.tree.genModel()
        response_status = BuildChatTemplateResponse()
        response_status.status = 10
        return response_status

    def GetQuestion(self, request, context):
        response = QuestionResponse()
        if self.cur_node is None:
            self.cur_node = self.tree.root
            self.resetSlot()
        else:
            print(request.answer)
            self.tmp_node = self.cur_node.getNode(request.answer)
            if self.cur_node.slot is not None:
                self.slot_dict[self.cur_node.slot] = self.cur_node.slot_info
            self.cur_node = self.tmp_node
        if self.cur_node is None:
            response.status = 2
            response.task_id = request.task_id
        else:
            response.question = self.cur_node.qs
            response.question_id = self.cur_node.qs_id
            if self.cur_node.isLeafNode():
                response.status = 2
            else:
                response.status = 1
            response.task_id = request.task_id
            response.need_answer = self.cur_node.need_answer
        print(response.question)
        return response

    def CloseChatTemplate(self, request, context):

        # todo: close session
        response = CloseChatTemplateResponse()
        response.info.info = str(self.slot_dict)
        response.status = 2
        return response




def test_ChatBotService():
    tree = build_intention_tree()
    service_node = ChatBotService()
    service_node.BuildChatTemplate(tree, None)
    print('hello world!')

if __name__ == '__main__':
    test_ChatBotService()


