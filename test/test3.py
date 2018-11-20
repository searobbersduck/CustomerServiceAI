import socket

ip = input("请输入您想连接的主机IP:")
port = int(input("请输入您想连接的主机端口:"))
while True:
    # 连接
    # socket.socket(通信方式,套接字类型)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((ip, port))
    # 发送数据
    keywd = input("请输入您要咨询的问题:")
    if (keywd == "end"):
        break
    bstring = keywd.encode("utf-8")
    sock.sendall(bstring)
    # 接收服务端返回的数据
    rst = sock.recv(2048).decode("utf-8")
    print("客服回复:" + str(rst))

sock.close()
