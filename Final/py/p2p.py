"""****************************************************************************************
 ** FileName:       p2p.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-06-29 星期六 18:29:29
 ** Description:    实现对等交流
 ****************************************************************************************"""
from Diffie_Hellman import key_generate, get_key
from client import Client
from server import Server
from random import randint
from data_signature_sm2 import authen, signature
import datetime
from ctr_mode import ctr_encode, ctr_decode
import threading

class p2p_server:
    __name = None                   # p2p的姓名
    __socket_ca = None              #实现对于公钥证书的套接字
    __socket_server = None             #实现对于对等方的服务器端
            #采用Diff——Hellman密钥交换来协商(ecc上的) 使用aes的ctr模式加密
    __k = None                      #协商的密钥 密钥k
    __t = None                      #协商的密钥 计数器t
    __identiter = None              #证书
    __ip_ca = None
    __port_ca = None
    __client_ip = None
    __client_port = None
    __ca_key = None
    __socket_client = None
    __socket_client_ip = None
    __socket_client_port = None
    __mutex = threading.Semaphore(1)
    __mutex_client = threading.Semaphore(1)
    __mutex_server = threading.Semaphore(1)
    __isquit = False
    __mutex_isquit = threading.Semaphore(1)
    

    def init(self, name, ip, port, ip_ca, port_ca, ca_key):
        self.__name = name
        self.__ip_ca = ip_ca
        self.__port_ca = port_ca
        self.__socket_server = Server(ip, port)
        self.__socket_ca = Client()
        self.__ca_key = ca_key
    
    def __get_from_ca(self):
        res = self.__socket_ca.tcp(self.__ip_ca, self.__port_ca, '{0}:find'.format(self.__name))
        return res

    def negotiation_key(self, client_ip, client_port, *, ddl = None, k = None, pk = None):
        print("——————————————————开始协商密钥—————————————————————")
        try:
            if(ddl != None and k == None and pk == None):
                k, pk = key_generate()
                print("生成公钥:{0} 私钥:{1}".format(str(pk), str(k)))
                print("(可直接复制到CA命令中){2} {1} {0}".format(ddl, str(pk[0]) + "|" + str(pk[1]), self.__name))
                input("确认生成信息：(复制到CA命令后，按一下回车即可)")
            elif(ddl == None and pk != None and k != None):
                print("接收输入参数")
            else:
                print("参数输入错误！")
                raise Exception

            self.__client_ip, self.__client_port, pk_client = self.__socket_server.recv()
            self.__socket_server.send(str(pk[0]) + ' ' + str(pk[1]))
            pk_client_x, pk_client_y = map(int, pk_client.split(" "))
            
            self.__client_ip, self.__client_port, certificate_client = self.__socket_server.recv()
            certificate = self.__get_from_ca()
            self.__socket_server.send(certificate)
            

            print('从{0}收到的证书为:{1}'.format(self.__client_ip + ':' + str(self.__client_port), certificate_client))
            name, message, sign = certificate_client.split(" ")

            sign_x, sign_y = sign.split(":")
            data, name, key = message.split(":")
            data = datetime.datetime.strptime(data, "%Y-%m-%d")
            point_x, point_y = map(int, key.split("|"))
            if(point_x != pk_client_x or point_y != pk_client_y):
                print("公钥不匹配或公钥与证书不匹配！")
                raise Exception

            self.__client_ip, self.__client_port, client_name = self.__socket_server.recv()
            self.__socket_server.send(self.__name)

            sign = (sign_x, sign_y)
            if(client_name == name and authen(message, sign, name, self.__ca_key) and data >= datetime.datetime.now()):
                point = get_key(point_x, point_y, k)
                key = (hex((point[0] ^ point[1]))[2:]).zfill(32)
                self.__k = key[:32]
                key = (hex((point[0] & point[1]))[2:]).zfill(32)
                self.__t = key[:32]
                print("密钥协商成功:密钥k：{0} 计数器：{1}".format(self.__k, self.__t))
                self.__t = int(self.__t, 16)
                self.__socket_client = Client()
                self.__client_ip = client_ip
                self.__client_port = client_port
                return True
            else:
                print("密钥协商失败！")
                raise Exception
        except:
            print("{0}协商失败！".format(self.__name))
            self.__socket_server.close()
            self.__socket_client.close()
            self.__k = None
            self.__t = None            
    
    def __receive_func(self):
        try:
            while(True):
                ip, port, message = self.__socket_server.recv()
                self.__socket_server.send(" ")

                print("\n密文: {2} 解密密钥key:{0}, t = {1}".format(self.__k, self.__t, message), end = ' ')
                self.__mutex.acquire()
                self.__t, message = ctr_decode(message, self.__k, self.__t)
                self.__mutex.release()
                print("解密结果:" + message)
                if(message == 'quit'):
                    raise Exception
        except:
            self.__mutex_isquit.acquire()
            if(self.__isquit == False):
                print("连接中断!出现错误\n请键入\'quit\'!!!!")
                self.__isquit = True
            self.__mutex_isquit.release()
            self.__mutex_server.release()

    def __send_func(self):
        try:
            isquit = False
            while(True):
                message = input("\n请输入所要发送的语句:")
                
                if(message == 'quit'):
                    isquit = True
                self.__mutex.acquire()
                print("加密密钥：key = {0}, t = {1}:".format(self.__k, self.__t), end = "")
                self.__t, message = ctr_encode(message, self.__k, self.__t)
                self.__mutex.release()
                self.__socket_client.tcp(self.__client_ip, self.__client_port, message)
                print("加密结果:{0}".format(message))
                if(isquit):
                    self.__mutex_isquit.acquire()
                    self.__isquit = True
                    self.__mutex_isquit.release()
                    print("请等待对方结束通信！")
                    raise Exception
        except:
            self.__mutex_client.release()

    

    def run(self):
        self.__mutex_client.acquire()
        self.__mutex_server.acquire()
        thread1 = threading.Thread(target=self.__receive_func)
        thread1.start()
        thread2 = threading.Thread(target=self.__send_func)
        thread2.start()
        self.__mutex_client.acquire()
        self.__mutex_server.acquire()
        self.__socket_client.close()
        self.__socket_server.close()
        self.__k = None
        self.__t = None
        self.__isquit = False
        self.__mutex._value = 1
        self.__mutex_client._value = 1
        self.__mutex_isquit._value = 1
        self.__mutex_server._value = 1
        print("——————————————————————————通信结束——————————————————————————")

        

        
class p2p_client:
    __name = None                   # p2p的姓名
    __socket_ca = None              #实现对于公钥证书的套接字
    __socket_client = None             #实现对于对等方的服务器端
            #采用Diff——Hellman密钥交换来协商(ecc上的)
    __k = None                      #协商的密钥
    __t = None                      #协商的密钥 计数器t
    __identiter = None              #证书
    __ip_ca = None
    __port_ca = None
    __ca_key = None
    __ip_server = None
    __port_server = None
    __socket_server = None
    __mutex = threading.Semaphore(1)
    __mutex_client = threading.Semaphore(1)
    __mutex_server = threading.Semaphore(1)
    __isquit = False
    __mutex_isquit = threading.Semaphore(1)

    def init(self, name, ip_ca, port_ca, ca_key, client_ip, client_port):
        self.__name = name
        self.__ip_ca = ip_ca
        self.__port_ca = port_ca
        self.__socket_client = Client()
        self.__socket_ca = Client()
        self.__ca_key = ca_key
        self.__socket_server = Server(client_ip, client_port)
    
    def __get_from_ca(self):
        res = self.__socket_ca.tcp(self.__ip_ca, self.__port_ca, '{0}:find'.format(self.__name))
        return res


    def negotiation_key(self, server_ip, server_port, *, ddl = None, k = None, pk = None):
        try:
            print("——————————————————开始协商密钥—————————————————————")
            if(ddl != None and k == None and pk == None):
                k, pk = key_generate()
                print("生成公钥:{0} 私钥:{1}".format(str(pk), str(k)))
                print("(可直接复制到CA命令中){2} {1} {0}".format(ddl, str(pk[0]) + "|" + str(pk[1]), self.__name))
                input("确认生成信息：(复制到CA命令后，按一下回车即可)")
            elif(ddl == None and pk != None and k != None):
                print("接收输入参数")
            else:
                self.__socket_client.close()
                print("参数输入错误！")
                raise Exception

            pk_server = self.__socket_client.tcp(server_ip, server_port, str(pk[0]) + " " + str(pk[1]))
            pk_server_x, pk_server_y = map(int, pk_server.split(" "))

            certificate = self.__get_from_ca()
            certificate_server = self.__socket_client.tcp(server_ip, server_port, certificate)
            print('从{0}收到的证书为:{1}'.format(server_ip + ':' + str(server_port), certificate_server))

            server_name = self.__socket_client.tcp(server_ip, server_port, self.__name)

            name, message, sign = certificate_server.split(" ")
            sign_x, sign_y = sign.split(":")
            data, name, key = message.split(":")
            data = datetime.datetime.strptime(data, "%Y-%m-%d")
            point_x, point_y = map(int, key.split("|"))
            if(point_x != pk_server_x or point_y != pk_server_y):
                print("公钥不匹配或公钥与证书不匹配！")
                raise Exception

            sign = (sign_x, sign_y)

            if(name == server_name and authen(message, sign, name, self.__ca_key) and data >= datetime.datetime.now()):
                point = get_key(point_x, point_y, k)
                key = (hex((point[0] ^ point[1]))[2:]).zfill(32)
                self.__k = key[:32]
                key = (hex((point[0] & point[1]))[2:]).zfill(32)
                self.__t = key[:32]
                print("密钥协商成功:密钥k：{0} 计数器：{1}".format(self.__k, self.__t))
                self.__t = int(self.__t, 16)
                self.__ip_server = server_ip
                self.__port_server = server_port
                return True
            else:
                self.__socket_client.close()
                print("{0}协商失败！".format(self.__name))
                raise Exception
            
        except:
            self.__socket_client.close()
            print("密钥协商失败！")
            return None

    def __receive_func(self):
        try:
            while(True):
                ip, port, message = self.__socket_server.recv()
                self.__socket_server.send(" ")
                print("\n接收到的加密消息:{0}".format(message))
                self.__mutex.acquire()
                print("解密密钥key:{0}, t = {1}".format(self.__k, self.__t), end = ' ')
                self.__t, message = ctr_decode(message, self.__k, self.__t)
                self.__mutex.release()

                print(" 解密结果:{0}".format(message))
                if(message == 'quit'):
                    raise Exception
        except:
            
            self.__mutex_isquit.acquire()
            if(self.__isquit == False):
                print("连接中断!出现错误\n请键入\'quit\'!!!!")
                self.__isquit = True
            self.__mutex_isquit.release()
            self.__mutex_server.release()

    
    def __send_func(self):
        try:
            isquit = False
            while(True):
                message = input("请输入信息:")
                if(message == 'quit'):
                    isquit = True
                self.__mutex.acquire()
                print("\n加密密钥：key = {0}, t = {1}:".format(self.__k, self.__t), end = "")
                self.__t, message = ctr_encode(message, self.__k, self.__t)
                self.__mutex.release()
                self.__socket_client.tcp(self.__ip_server, self.__port_server, message)
                
                print(" 加密结果:{0}".format(message))
                if(isquit):
                    self.__mutex_isquit.acquire()
                    self.__isquit = True
                    self.__mutex_isquit.release()
                    print("请等待对方结束通信！")
                    raise Exception
        except:
            
            self.__mutex_client.release()



    def run(self):
        self.__mutex_client.acquire()
        self.__mutex_server.acquire()
        thread1 = threading.Thread(target=self.__receive_func)
        thread1.start()
        thread2 = threading.Thread(target=self.__send_func)
        thread2.start()
        self.__mutex_client.acquire()
        self.__mutex_server.acquire()
        self.__socket_client.close()
        self.__socket_server.close()
        self.__k = None
        self.__t = None
        self.__isquit = False
        self.__mutex._value = 1
        self.__mutex_client._value = 1
        self.__mutex_isquit._value = 1
        self.__mutex_server._value = 1
        print("——————————————————————————通信结束——————————————————————————")



        


if(__name__ == '__main__'):
    sk = 37838632701420116879821850903800472393345025014084230001515186363471476114639
    pk = (48512027864650021867681261707378924189222238041537180459913491423973706385315, 12347006614419446767777325628942602486721496981580611877273353936539536025074)
    sig = signature("sdasdsad:s", "asd", sk)
    print(authen("sdasdsad:s", sig, "asd", pk))

        