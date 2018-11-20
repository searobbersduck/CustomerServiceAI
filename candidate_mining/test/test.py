from test_pb2 import *

node = ChatNode()

keys = PathKeys()

keys.keys.append('是')

keys.keys.append('对')

node.keys['是'].CopyFrom(keys)
node.keys['不是'].keys.append('不是')

node.children['是'].CopyFrom()

print('hello world!')