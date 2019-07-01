"""****************************************************************************************
 ** FileName:       client.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-06-28 星期五 17:23:55
 ** Description:    实现客户端
 ****************************************************************************************"""

import socket

class Client:

    __socket_tcp = None
    def close(self):
        if(self.__socket_tcp != None):
            self.__socket_tcp.close()

    def tcp(self, ip, port, message):
        try:
            self.__socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket_tcp.connect((ip, port))
            socket_name = self.__socket_tcp.getsockname()
            self.__socket_tcp.send(message.encode(encoding = 'utf-8'))
            message = self.__socket_tcp.recv(1024)
            message = message.decode(encoding = 'utf-8')
            self.__socket_tcp.close()
            return message
        except:
            print("连接异常")
            self.close()
    
    


    

            
