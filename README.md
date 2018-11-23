# CustomerServiceAI
智能客服

## demo
[一个客服系统的demo](./candidate_mining/test/readme.md)

## Reference
1. [python 使用gensim和pickle包，模拟智能客服系统](https://blog.csdn.net/a394268045/article/details/79208023)
2. [填槽与多轮对话 | AI产品经理需要了解的AI技术概念](https://mp.weixin.qq.com/s?__biz=MjM5NzA5OTAwMA==&mid=2650005853&idx=1&sn=2c6bb9e9c3751fdc3fd95e89b8b6377d&chksm=bed865ca89afecdcdf0ecde9ed2385fb613cb2a40ad0c491582c7faf91841d17efdfe59718e1&mpshare=1&scene=1&srcid=0304keVTiRXgpPHVGxGFL6mI#rd)
3. [Chatbot中的填槽(Slot Filling)](https://blog.csdn.net/u010159842/article/details/80759428)
4. todo: 意图树  搜索意图树相关的内容  基于此开始看起
5. [基于机器学习的阿里智能助理](https://data.hackinn.com/ppt/2016%E6%9D%AD%E5%B7%9E%E4%BA%91%E6%A0%96%E5%A4%A7%E4%BC%9A/%E5%BC%80%E5%8F%91%E8%80%85%E6%8A%80%E6%9C%AF%E5%B3%B0%E4%BC%9A-%E6%9E%B6%E6%9E%84/%E9%98%BF%E9%87%8C%E6%99%BA%E8%83%BD%E5%8A%A9%E7%90%86%E5%9C%A8%E7%94%B5%E5%95%86%E9%A2%86%E5%9F%9F%E7%9A%84%E6%9E%B6%E6%9E%84%E6%9E%84%E5%BB%BA%E4%B8%8E%E5%AE%9E%E8%B7%B5.pdf)




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
![start server](./candidate_mining/test/img/chatbot_server.gif)
3. 启动Client, **``python chatbot_client.py``**, 如果要用语音版本，请运行**``python chatbot_client_speech.py``**
![start client](./candidate_mining/test/img/chatbot_client.gif)

## 效果
![效果](./candidate_mining/test/img/chatbot_dialog.gif)