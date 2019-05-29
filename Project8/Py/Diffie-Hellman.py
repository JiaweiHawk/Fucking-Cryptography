"""****************************************************************************************
 ** FileName:       Diffie-Hellman.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-15 星期三 21:56:01
 ** Description:    实现Diffie-Hellman的双人密钥交换协议
                    即使用多线程来模拟双方的收发情况
 ****************************************************************************************"""

from ecc import ecc_mul, G, G_n
from random import randint
import threading
import queue

"""****************************************************************************************
 ** Date:           2019-05-15 星期三 22:12:18
 ** Description:    Alice()函数来模拟课本中Alice的行为
 ****************************************************************************************"""

def user(name, queue_self, queue_other, sem):
    k = randint(2, G_n[0])
    pk_self = ecc_mul(G[0], k)
    queue_other.put(pk_self)
    while(queue_self.empty() == True):
        continue
    pk_other = queue_self.get()

    sem.acquire()
    print(name + '生成的随机私钥是:' + str(k))
    print(name + '生成的公钥是是:' + str(k))
    print('x = ' + str(pk_self[0]) + ' y = ' + str(pk_self[1]))

    print(name + '接收到的公钥是:')
    print('x = ' + str(pk_other[0]) + ' y = ' + str(pk_other[1]))

    print(name + '最终得到的协商密钥是:')

    k = ecc_mul(pk_other, k)
    print('x = ' + str(k[0]) + ' y = ' + str(k[1]))
    print('---------------------------------------------------------------------------------'\
    '-------------------------------------------------------------------------------------\n')
    sem.release()



queue_Alice = queue.Queue()
queue_Bob = queue.Queue()
sem = threading.Semaphore(value = 1)

thread_Alice = threading.Thread(target=user, args=('Alice', queue_Alice, queue_Bob, sem))
thread_Alice.start()
thread_Bob = threading.Thread(target=user, args=('Bob', queue_Bob, queue_Alice, sem))
thread_Bob.start()


