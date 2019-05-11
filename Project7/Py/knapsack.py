"""****************************************************************************************
 ** FileName:       knapsack.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-08 星期三 16:13:29
 ** Description:    实现背包密码体制及其攻击
 ****************************************************************************************"""

from knapsack_math import euc_ext
from random import randint
from copy import deepcopy



"""****************************************************************************************
 ** Date:           2019-05-09 星期四 08:49:11
 ** Description:    生成超递增背包序列并保存在文件中
 ****************************************************************************************"""


key_size = [None] * 1
n = [None] * 1
pk = None
sk = [None] * 1

def key_generate():

    pk = [None] * key_size[0]
    pk[0] = randint(1, key_size[0])
    sum_sk = pk[0]

    for i in range(1, key_size[0]):
        pk[i] = randint(sum_sk + 1, sum_sk << 1)
        sum_sk = sum_sk + pk[i]

    # 为了便于计算  让模数n等于b[length] * 2 + 1
    n[0] = ((pk[-1]) << 1) + 1
    w = randint(2, n[0])
    tmp = euc_ext(w, n[0])
    while( tmp[2] != 1):
        w = randint(2, n[0])
        tmp = euc_ext(w, n[0])
    sk[0] = tmp[0]          #

    out = open("key.knapsack", "w")

    out.write("n的值")
    out.write('\n')
    out.write(str(n[0]))        #   n的值
    out.write('\n')
    
    out.write("公钥部分")
    out.write('\n')
    for i in range(key_size[0]):
        out.write(str((pk[i] * w) % n[0]))
        out.write(' ')
    out.write('\n')


    out.write("私钥部分")
    out.write('\n')
    out.write(str(tmp[0] % n[0]))        #   w的逆的值
    out.write('\n')
    
    print("生成密钥成功\n")
    
    out.close()



def get_key(flag):                      #如果为0表示读取公钥，如果为1表示读取私钥
    global pk
    try:
        file_key = open("key.knapsack", "r")
    except IOError:
        print("Error, File not found")
        exit()

    if(flag == 1):
        print("------------------------------开始读取私钥------------------------------------")
    else:
        print("------------------------------开始读取公钥------------------------------------")

    while(file_key.readline() != "n的值\n"):
        file_key.readline()
    n[0] = int(file_key.readline())

    while(file_key.readline() != "公钥部分\n"):
        file_key.readline()
    pk = list(map(int, (file_key.readline().split(" "))[:-1]))

    if(flag == 1):
        while(file_key.readline() != "私钥部分\n"):
            file_key.readline()
        sk[0] = int(file_key.readline())

    file_key.close()
    if(flag == 1):
        print("------------------------------私钥读取成功------------------------------------")
    else:
        print("------------------------------公钥读取成功------------------------------------")


def encode():    #message为要加密的特定大小的二进制文件   
    print("------------------------------开始加密------------------------------------")    
    get_key(0)          #读取公钥用来加密
    try:
        file_in = open("message.png", "rb")
    except IOError:
        print("Error! File not exits")
        exit()
    size = key_size[0] >> 3
    
    number = size << 3

    file_out = open("cipher.knapsack", "w")
    message = file_in.read(size).hex()

    while(message != ''):
        file_out.write(str(len(message)))        #发送读取时写的长度
        file_out.write(' ')

        message = int(message, 16)
        tmp = 0
        for i in range(number):
            tmp = tmp + ((message >> (number - 1 - i)) & 1) * pk[i]


        file_out.write(str(tmp % n[0]))
        file_out.write('\n')
        message = file_in.read(size).hex()

    file_in.close()
    file_out.close()
    print("------------------------------加密成功------------------------------------") 
    
    
def decode():    #message为要解密的特定大小的二进制文件
    print("------------------------------开始解密------------------------------------")    
    get_key(1)          #读取私钥用来解密
    try:
        file_in = open("cipher.knapsack", "r")
    except IOError:
        print("Error! File not exits")
        exit()
    
    for i in range(key_size[0]):
        pk[i] = (pk[i] * sk[0]) % n[0]

    size_write = None
    number = (key_size[0] >> 3) << 3


    file_out = open("message_knapsack.png", "wb")

    cipher = file_in.readline()
    while(cipher != ''):
        cipher = cipher.split()
        size_write = int(cipher[0])
        cipher = (int(cipher[1]) * sk[0]) % n[0]

        tmp = 0
        for i in range(number - 1, -1, -1):
            if(cipher >= pk[i]):
                tmp = tmp | (1 << (number - i - 1))
                cipher = cipher - pk[i]
        file_out.write(bytes.fromhex((hex(tmp)[2:]).zfill(size_write)))
        cipher = file_in.readline()



    print("------------------------------解密成功------------------------------------") 
    file_in.close()
    file_out.close()


def is_super_increment(w_inv):                  #判断w_inv能否生成超递增序列
    key = deepcopy(pk)
    for i in range(key_size[0]):
        key[i] = (key[i] * w_inv) % n[0]

    if(n[0] <= 2 * key[-1]):         #首先判断最大的那个数的二倍是否小于模数n
        return None
    
    sum_serial = 0
    for i in range(1, key_size[0]):
        if(key[i] <= sum_serial):
            return None
        sum_serial = sum_serial + key[i]
    

    print("w_inv = {0},攻击构造的超递增序列：".format(str(w_inv)), end = ' ')
    print(key)


    return key


def attack():
    print("------------------------------开始攻击------------------------------------") 
    get_key(0)                      #获取公钥
    print("------------------------------开始构造超递增序列------------------------------------")
    for i in range(1, n[0]):
        key = is_super_increment(i)
        if(key != None):
            break
    # 和decode的函数一样
    try:
        file_in = open("cipher.knapsack", "r")
    except IOError:
        print("Error! File not exits")
        exit()

    size_write = None
    number = (key_size[0] >> 3) << 3


    file_out = open("message_knapsack_attack.png", "wb")

    cipher = file_in.readline()
    while(cipher != ''):
        cipher = cipher.split()
        size_write = int(cipher[0])
        cipher = (int(cipher[1]) * sk[0]) % n[0]

        tmp = 0
        for i in range(number - 1, -1, -1):
            if(cipher >= key[i]):
                tmp = tmp | (1 << (number - i - 1))
                cipher = cipher - key[i]
        file_out.write(bytes.fromhex((hex(tmp)[2:]).zfill(size_write)))
        cipher = file_in.readline()



    print("------------------------------攻击成功------------------------------------")
    file_in.close()
    file_out.close()





if(__name__ == '__main__'):
    key_size[0] = int(input("请输入背包密钥的序列个数(>= 8):"))
    while(key_size[0] < 8):
        key_size[0] = int(input("请输入背包密钥的序列个数(>= 8):"))
    key_generate()
    encode()
    print("")
    attack()
    print("")
    decode()