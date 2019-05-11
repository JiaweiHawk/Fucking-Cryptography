"""****************************************************************************************
 ** FileName:       oaep_math.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-10 星期五 19:25:04
 ** Description:    提供对于RSA的最优非对称加密填充算法的加解密的数学基础
                    全部接口以16进制字符串,且长度应该为固定的偶数
 ****************************************************************************************"""

from hashlib import sha1
from random import randint


h_len = [20]                       # 选用的hash函数是SHA-1, 8位分组长度为20
n_size = [None] * 1                 # 模数n的bit长度

"""****************************************************************************************
 ** Date:           2019-05-10 星期五 21:17:04
 ** Description:    编码的hash算法
 ****************************************************************************************"""

# 当p为空时, ihash: da39a3ee 5e6b4b0d 3255bfef 95601890 afd80709
def hash(p):
    if (p == None):
        return 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
    if(len(p.encode()) > 2 ** 64 - 8):
        print("P is too Long")
        exit()
    hash_func = sha1()
    hash_func.update(p.encode())
    return hash_func.hexdigest()



"""****************************************************************************************
 ** Date:           2019-05-10 星期五 21:17:04
 ** Description:    生成DB序列
 ****************************************************************************************"""


def db_generate(p, m):
    k = (n_size[0] >> 3)
    m = bytes(m, encoding = 'utf-8').hex()
    m_len = (len(m) + 1) >> 1
    m = m.zfill(m_len << 1)
    if(m_len > k - 2 * h_len[0] - 2):
        print("Message too long")
        exit()
    length = k - 2 - 2 * h_len[0] - m_len
    return hash(p) + '00' * length + '01' + m



"""****************************************************************************************
 ** Date:           2019-05-10 星期五 21:17:04
 ** Description:    MGF函数
 ****************************************************************************************"""
# x为非负数,xlen为8位组串长度,我们输出为16进制的
def I2OSP(x, xlen):
    if(x >= 256 ** xlen):
        print("x is too big")
        exit()
    out = [None] * xlen
    for i in range(xlen):
        out[i] = (hex(x & 255)[2:]).zfill(2)
        x = x >> 8
    return ''.join(out)

def OSP2I(x):
    out = 0
    for i in range(0, len(x), 2):
        tmp = int(x[-2:], 16)
        out = (out << 8) + tmp
        x = x[:-2]
    return out

def mgf(mgfseed, masklen):
    if(masklen > h_len[0] * (2 ** 32)):
        print("masklen is too long")
        exit()
    out = ''
    for counter in range(int((masklen + h_len[0] - 1)// h_len[0])):
        out = out + hash(mgfseed + I2OSP(counter, 4))
    return out[:masklen << 1]

# message 为正常人类语言而非16进制
def em_encode(p, message):
    db = db_generate(p, message)
    seed = randint(0, 2 ** h_len[0] - 1)
    seed_hex = (hex(seed)[2:]).zfill(h_len[0] << 1)
    maskeddb = (hex(int(mgf(seed_hex, h_len[0]), 16) ^ int(db, 16))[2:]).zfill(((n_size[0] >> 3) - h_len[0] - 1) << 1)
    maskedseed = (hex(seed ^ int(mgf(maskeddb, h_len[0]), 16))[2:]).zfill(h_len[0] << 1)
    return '00' + maskedseed + maskeddb

# 输出em 为正常人类语言而非16进制
def em_decode(em):
    maskedseed = em[2: 2 + (h_len[0] << 1)]
    maskeddb = em[2 + (h_len[0] << 1):]
    seed_hex = (hex(int(maskedseed, 16) ^ int(mgf(maskeddb, h_len[0]), 16))[2:]).zfill(h_len[0] << 1)
    db = (hex(int(maskeddb, 16) ^ int(mgf(seed_hex, h_len[0]), 16))[2:]).zfill(((n_size[0] >> 3) - h_len[0] - 1) << 1)
    db = db[(h_len[0] << 1):]
    while(db[:2] != '01'):
        db = db[2:]
    return bytes.fromhex(db[2:]).decode(encoding = 'utf-8')


if(__name__ == '__main__'):
    n_size[0] = int(input("the bit-length of the n:"))
    em = em_encode(None, input("input the message:"))
    print('the message is:' + em_decode(em))
