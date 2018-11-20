# !/usr/bin/env python3

import grpc
import time
from concurrent import futures
import candidate_info_pb2, candidate_info_pb2_grpc
from intention_tree import *

class ChatBotService(candidate_info_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.name = ChatBotService()
        self.node = None
        self.tree = IntentionTree()

    def getNode(self, grpc_node):
        node = IntentionTreeNode(grpc_node.qs, grpc_node.qs_id, grpc_node.slot)
        for i in node.children.size():
            child_node = getNode(node.children[i].node)
            node.insertNode(node.children[i].choice, child_node)
            for sent in node.children[i].keys:
                node.insertConds(node.children[i].choice, sent)
        return node

    def BuildChatTemplate(self, request, context):
        root_node = request.root
        node = getNode(root_node)
        self.tree.root = node
        self.tree.genModel()




