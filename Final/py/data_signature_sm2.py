"""****************************************************************************************
 ** FileName:       data_signature_sm2.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-30 星期四 16:14:55
 ** Description:    实现SM2的数字签名算法
                    其所有接口若无特殊说明
                    皆为16进制
 ****************************************************************************************"""

from sha1 import hash_sha1
from sha3 import hash_sha3
from data_signature_sm2_math import bit2bytes_string, bytes_string2bit, point2bytes_string, \
    field2bytes_string, bytes_string2point, bytes_string2int, int2bytes_string,\
    euc_ext
from ecc import ecc_mul, G, p, p_len, G_n, ecc_add, Infin
from random import randint
import threading

v = [160, 256]         #v[0]指密钥杂凑算法的输出bit数，v[1]表示加密时的Hash函数输出bit数
mode = [None]

"""****************************************************************************************
 ** Date:           2019-05-18 星期六 14:55:34
 ** Description:    加密方的组件
                    包括KDF算法（其中hash函数选择Sha1()，可以随意修改成其他的)
                    读取公钥。
 ****************************************************************************************"""

def key_generate():
    while(True):
        d = randint(1, G_n[0] - 2)
        pk = ecc_mul(G[0], d)
        if(pk == Infin[0]):
            continue
        return d, pk
    return None
    




# 一些没有必要的过程进行简化, 部分过程标准文档过于麻烦则简化了
# za为关于用户 A 的可辨别标识、部分椭圆曲线系统参数和用户 A 公钥的杂凑值
# k为用户A随机选择的点
# da用户A的私钥。 
def signature(message, za, da): # 签名算法， 对消息进行签名

    while(True):
        k = randint(1, G_n[0] >> 1)
        message = za + message
        
        e = bytes_string2int(hash_sha3(bytes(message, encoding = 'utf-8'), v[1]))

        pa = ecc_mul(G[0], k)

        x1 = pa[0]              # 此步骤为转化pa的点为整形

        r = (e + x1) % G_n[0]
        if(r == 0 or (r + k) == G_n[0]):
            continue
        
        s = (euc_ext(1 + da, G_n[0])[0] * (k - r * da)) % G_n[0]

        if(s == 0):
            continue

        break

    return (field2bytes_string(r), field2bytes_string(s))



def authen(message, signa, za, pa):

    r = bytes_string2int(signa[0])
    if(r >= G_n[0] or r < 1):
        print('Authencation Failure')
        return None

    s = bytes_string2int(signa[1])
    if(s >= G_n[0] or s < 1):
        print('Authencation Failure')
        return None

    m = za + message
    m = bytes(m, encoding = 'utf-8')
    e = bytes_string2int(hash_sha3(m, v[1]))
    t = (r + s) % G_n[0]
    if(t == 0):
        print('Authencation Failure')
        return None
    point = ecc_add(ecc_mul(G[0], s), ecc_mul(pa, t))
    
    x1 = bytes_string2int(field2bytes_string(point[0]))
    R = (e + x1) % G_n[0]

    if(R == r):
        return True
    
    print('Authencation Failure')
    return None

