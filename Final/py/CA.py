"""****************************************************************************************
 ** FileName:       CA.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-06-28 星期五 10:19:09
 ** Description:    实现公钥证书及其标准
 ****************************************************************************************"""
from server import Server
from data_signature_sm2 import key_generate, signature, authen
import os
import threading

class CA:
    __ca_ip = None            #CA的ip
    __ca_port = None          #CA的port
            # ip + port 可以唯一识别
    __ca_sk = None            #CA的私钥       类型： 16进制
    __ca_encode_kind = None   #CA的加密方式    类型：字符串（例如：SHA3-256）
    __ca_data = None    #CA的数据的位置  类型：文件名
    __ca_data_name = None
    __ca_server = None        #CA的服务器端
    __ca_k = (48512027864650021867681261707378924189222238041537180459913491423973706385315, 12347006614419446767777325628942602486721496981580611877273353936539536025074)
    __mutex = threading.Semaphore(1)
    '''
        对CA进行初始化，包括名称、唯一ID、私钥、公私钥所用的加密方法、数据存放位置
    '''

    def init(self, ca_ip, ca_port, ca_sk, ca_encode_kind, ca_data_place):
        try:
            self.__ca_ip = ca_ip
            self.__ca_port = ca_port
            self.__ca_sk = ca_sk
            self.__ca_encode_kind = ca_encode_kind
            self.__ca_data_place = ca_data_place
            self.__ca_data_name = ca_data_place
            self.__ca_server = Server(ca_ip, ca_port)
            self.__ca_data = open(ca_data_place, "a+")
            print("初始化成功！")
        except:
            print("初始化失败！")


    '''
        公钥证书为:E(prauth, [T || IDA || name])
        存储形式为name, 公钥证书
    ''' 

    def __find(self, name):
        self.__mutex.acquire()
        self.__ca_data.seek(0)
        message = self.__ca_data.readline()
        while(message != ''):
            pu = (message[:-1].split(" "))[0]
            if( pu == name):
                self.__mutex.release()
                return message
            message = self.__ca_data.readline()
        self.__mutex.release()
        return None
    
    def __insert(self):
        while True:
            name, pka, time = input("请输入要添加的信息(姓名 公钥 有效时间):").split(" ")
            message = time + ':' + name + ":" + pka
            sign = signature(message, name, self.__ca_sk)
            self.__ca_data.seek(0)
            notfind = True

            self.__mutex.acquire()
            replace = open(self.__ca_data_name + "1", "w")
            line = self.__ca_data.readline()
            while(line != ''):
                pu = (line[:-1]).split(" ")[0]
                if(pu == name):
                    replace.write(name + ' ' + message + ' ' + sign[0] + ':' + sign[1] + '\n')
                    notfind = False
                else:
                    replace.write(line)
                line = self.__ca_data.readline()
            if(notfind):
                replace.write(name + ' ' + message + ' ' + sign[0] + ':' + sign[1] + '\n')
            replace.close()
            self.__ca_data.close()
            os.remove(os.path.abspath(self.__ca_data_name))
            os.rename(self.__ca_data_name + '1', self.__ca_data_name)
            self.__ca_data = open(self.__ca_data_name, "a+")

            self.__mutex.release()

    def insert(self):
        thread = threading.Thread(target=self.__insert)
        thread.start()

    def __run_func(self):
        while(True):
            try:
                ip, port, message = self.__ca_server.recv()
                print("\n从{0}收到消息：{1}".format((ip + ':' + str(port)), message))
                name, command = message.split(":")
                print(command)
                if(command == 'find'):
                    res = self.__find(name)
                    if(res == None):
                        self.__ca_server.send("Wrong!")
                        print("\n回复{0}：{1}".format((ip + str(port)), "Wrong!"))
                    else:
                        self.__ca_server.send("{0}".format(res))
                        print("\n回复{0}：{1}".format((ip + str(port)), res))
                else:
                    self.__ca_server.send("Wrong!")
                    print("\n回复{0}：{1}".format((ip + str(port)), "Wrong!"))
            except:
                continue

    def run(self):
        thread = threading.Thread(target=self.__run_func)
        thread.start()
            



if(__name__ == '__main__'):
    # pk, sk = key_generate()
    # 私钥 37838632701420116879821850903800472393345025014084230001515186363471476114639
    # 公钥 (48512027864650021867681261707378924189222238041537180459913491423973706385315, 12347006614419446767777325628942602486721496981580611877273353936539536025074)
    ca = CA()
    ca.init('127.0.0.1', 8989, 37838632701420116879821850903800472393345025014084230001515186363471476114639, "sm2", "data.txt")
    ca.insert()
    ca.run()