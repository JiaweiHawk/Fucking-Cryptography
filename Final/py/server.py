"""****************************************************************************************
 ** FileName:       client.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-06-28 星期五 17:23:55
 ** Description:    实现服务器端
 ****************************************************************************************"""

import socket

class Server:

    __socket_tcp = None
    __socket = None

    def __init__(self, ip, port):
        self.__socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_tcp.bind((ip, port))
        self.__socket_tcp.listen(1)

    def recv(self):
        try:
            self.__socket, addr = self.__socket_tcp.accept()
            message = self.__socket.recv(1024)
            message = message.decode(encoding = 'utf-8')
            return addr[0], addr[1], message
        except:
            
            self.close()
            print("服务器接收错误！")

    def send(self, message):
        try:
            self.__socket.send(message.encode(encoding = 'utf-8'))
        except:
            self.close()
            print("服务器发送错误")
    
    def close(self):
        if(self.__socket != None):
            self.__socket.close()

    

    

            
