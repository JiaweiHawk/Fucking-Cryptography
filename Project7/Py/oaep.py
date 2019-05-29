"""****************************************************************************************
 ** FileName:       oaep.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-08 星期三 16:15:06
 ** Description:    实现RSA的最优非对称加密填充算法的加解密
                    使用的hash函数为系统库自带的SHA-1
                    
 ****************************************************************************************"""

from oaep_math import em_encode, em_decode, n_size
from rsa_math import euc_ext, miller, qexp
from random import randint

n = [None] * 1
pk = [None] * 1
sk = [None] * 3
m = [None] * 2

"""****************************************************************************************
 ** Date:           2019-05-07 星期二 11:32:51
 ** Description:    实现2个输入互素的中国剩余定理
 ****************************************************************************************"""
def crt(m, sk):
    euc = euc_ext(sk[0], sk[1])
    return (euc[0] * sk[0] * m[1] + euc[1] * sk[1] * m[0]) % (n[0])



def n_generate():
    left = 2 ** (n_size[0] >> 1)
    right = (left << 2) - 1
    p = randint(left, right)
    while (miller(p) != True):
        p = randint(left, right)
    left = p << 2
    right = p << 4
    q = randint(left, right)
    while (miller(q) != True):
        q = randint(left, right)

    fai = (p - 1) * (q - 1)
    e = randint(1, fai)
    euc = euc_ext(e, fai)
    while (euc[2] != 1):
        e = randint(1, fai)
        euc = euc_ext(e, fai)
    pk[0] = e
    sk[0] = p
    sk[1] = q
    sk[2] = euc[0]
    n[0] = p * q

    n_size[0] = len(bin(p * q)) - 2


# message 为正常人类语言而非16进制, p为消息选项
def encode(p, message):
    em = em_encode(p, message)
    return hex(qexp(int(em, 16), pk[0], n[0]))[2:]

# message为加密后的十六进制数字字符串
def decode(cipher):
    cipher = int(cipher, 16)
    m[0] = qexp(cipher, sk[2] % (sk[0] - 1), sk[0])
    m[1] = qexp(cipher, sk[2] % (sk[1] - 1), sk[1])
    return em_decode((hex(crt(m, sk))[2:]).zfill((n_size[0] >> 3) << 1))

if(__name__ == '__main__'):
    n_size[0] = int(input("请输入密钥最少位数:"))
    n_generate()
    message = input("请输入消息和消息标志(可以不输入,若输入以空格隔开,并将最后一个当作消息标志):").split()
    if(len(message) == 1):
        cipher = encode(None, message[0])
    else:
        cipher = encode(message[-1], ' '.join(message[:-1]))
    print("加密的消息的16进制为:" + str(cipher))
    print('\nthe message is:' + decode(cipher))