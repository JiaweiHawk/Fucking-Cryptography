"""****************************************************************************************
 ** FileName:       hmac_sha1.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-24 星期五 23:11:32
 ** Description:    实现基于SHA1的HMAC算法
 ****************************************************************************************"""

from sha1 import hash_sha1
from sha3 import hash_sha3


B = {1:64, 224:144, 256:136, 384:104, 512:72}        # 对应模式


def ipad(n):    #'36' 重复n次
    return '36' * n


def opad(n):    #'36' 重复n次
    return '5c' * n


def Hash(message, hash_mode):   # message为16进制
    if(hash_mode == 1):
        return hash_sha1(bytes.fromhex(message))
    else:
        return hash_sha3(bytes.fromhex(message), hash_mode)

# k 为16进制， text为明文
def hamc(k, text, hash_mode):     # hash_mode = 1为SHA-1 hash_mode = 3为SHA3
    length = len(k) >> 1

    if(length == B[hash_mode]):
        k0 = k
    elif(length > B[hash_mode]):
        k0 = Hash(k, hash_mode) + '00' * (length - B[hash_mode])
    else:
        k0 = k + '00' * (B[hash_mode] - length)
    
    tmp1 = (hex(int(k0, 16) ^ int(ipad(B[hash_mode]), 16))[2:]).zfill(B[hash_mode])
    tmp1 = Hash(tmp1 + text, hash_mode)

    tmp2 = (hex(int(k0, 16) ^ int(opad(B[hash_mode]), 16))[2:]).zfill(B[hash_mode])

    return Hash(tmp2 + tmp1, hash_mode)
    

def show():
    file_in = open("message.txt", "r")
    message = ''
    tmp = file_in.readline()
    
    while(tmp != ''):
        message = message + tmp 
        tmp = file_in.readline()

    print('从message.txt文件中接收到的文本为:{0}'.format(message))

    message = bytes(message, encoding = 'utf-8').hex()

    file_in.close()
    file_in = open('hmac.key', 'r')
    key = file_in.readline()
    file_in.close()

    print('获取的密钥为:' + key)
    print('使用SHA1的HMAC为：{0}'.format(hamc(key, message, 1)))


    print('获取的密钥为:' + key)
    print('使用SHA3-224的HMAC为：{0}'.format(hamc(key, message, 224)))

    print('获取的密钥为:' + key)
    print('使用SHA3-256的HMAC为：{0}'.format(hamc(key, message, 256)))


    print('获取的密钥为:' + key)
    print('使用SHA3-384的HMAC为：{0}'.format(hamc(key, message, 384)))


    print('获取的密钥为:' + key)
    print('使用SHA3-512的HMAC为：{0}'.format(hamc(key, message, 512)))


if(__name__ == '__main__'):
    show()