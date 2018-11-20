# 一个客服系统的demo

## 实现功能
1. 打电话给候选人
    * 确认候选人
    * 是否有求职意向
    * 微信号是不是手机号
    
## 运行
运行环境python3
1. 编译proto, ***``python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./candidate_info.proto``***
2. 启动Server, **``python chatbot_server.py``**
![start server](./img/chatbot_server.gif)
3. 启动Client, **``python chatbot_client.py``**
![start client](./img/chatbot_client.gif)

## 效果
![效果](./img/chatbot_dialog.gif)