"""****************************************************************************************
 ** FileName:       rsa.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-07 星期二 11:18:49
 ** Description:    实现rsa基础算法
                    pk[0]是公钥n，pk[1]是公钥e
                    sk[0]是私钥d
 ****************************************************************************************"""
from rsa_math import euc_ext, miller, qexp
from random import randint

n = [None] * 1
pk = [None] * 1
sk = [None] * 1
n_size = [None] * 1


def n_generate():
    left = 2 ** (n_size[0] >> 1)
    right = (left << 2) - 1
    p = randint(left, right)
    while( miller(p) != True):
        p = randint(left, right)
    left = p << 2
    right = p << 4
    q = randint(left, right)
    while( miller(q) != True):
        q = randint(left, right)

    fai = (p - 1) * (q - 1)
    e = randint(1, fai)
    euc = euc_ext(e, fai)
    while(euc[2] != 1):
        e = randint(1, fai)
        euc = euc_ext(e, fai)
    d = euc[0] % fai

    n_size[0] = len(bin(p * q)) - 2

    # print('n的位数{0}'.format(str(len(bin(p * q)) - 2)))
    out = open("key.rsa", "w")
    out.write("n的位数")
    out.write('\n')
    out.write(str(n_size[0]))        #   n的位数
    out.write('\n')

    out.write("n的值")
    out.write('\n')
    out.write(str(p * q))        #   n的值
    out.write('\n')

    out.write("公钥部分")
    out.write('\n')
    out.write(str(e))        #   e的值
    out.write('\n')
    
    out.write("私钥部分")
    out.write('\n')
    out.write(str(d))        #   d的值
    out.write('\n')
    
    out.close()
    print("生成密钥成功\n")



def get_key(flag):                      #如果为0表示读取公钥，如果为1表示读取私钥

    try:
        file_key = open("key.rsa", "r")
    except IOError:
        print("Error, File not found")
        exit()
    try:
        while(file_key.readline() != "n的位数\n"):
            file_key.readline()
        n_size[0] = int(file_key.readline())
    except EOFError:
        print("File is wrong")
        exit()

    while(file_key.readline() != "n的值\n"):
        file_key.readline()
    n[0] = int(file_key.readline())

    if(flag == 1):
        while(file_key.readline() != "私钥部分\n"):
            file_key.readline()
        sk[0] = int(file_key.readline())
    else:
        while(file_key.readline() != "公钥部分\n"):
            file_key.readline()
        pk[0] = int(file_key.readline())
    # print(file_key.readline() == "n的值\n")

    file_key.close()
    print("密钥读取完毕\n")


def encode():       
    get_key(0)          #读取公钥用来加密
    try:
        file_in = open("message.png", "rb")
    except IOError:
        print("Error! File not exits")
        exit()
    size_read = ((n_size[0] - 1) >> 3) - 1
    size_write = ( (n_size[0] + 7) >> 3 ) * 2
    file_out = open("cipher.rsa", "wb")
    message = file_in.read(size_read).hex()
    while(message != ''):
        file_out.write(bytes.fromhex( (hex(qexp(int('11' + message, 16), pk[0], n[0]))[2:]).zfill(size_write) ))
        message = file_in.read(size_read).hex()
    file_in.close()
    file_out.close()
    print("加密成功\n")
    
    
def decode():      
    get_key(1)          #读取私钥用来解密
    try:
        file_in = open("cipher.rsa", "rb")
    except IOError:
        print("Error! File not exits")
        exit()
    size_read = (n_size[0] + 7) >> 3
    file_out = open("message_rsa.png", "wb")
    cipher = file_in.read(size_read).hex()
    while(cipher != ''):
        tmp = hex(qexp(int(cipher, 16), sk[0], n[0]))[2:]
        while(tmp[:2] != '11'):
            tmp = tmp[2:]
        file_out.write(bytes.fromhex(tmp[2:]))
        cipher = file_in.read(size_read).hex()
    print("解密成功\n")
    file_in.close()
    file_out.close()
    
    


if(__name__ == '__main__'):

    n_size[0] = int(input("请输入密钥最少位数:"))
    n_generate()
    encode()
    decode()