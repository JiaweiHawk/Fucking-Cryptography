"""****************************************************************************************
 ** FileName:       Diffie_Hellman.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-15 星期三 21:56:01
 ** Description:    实现diffie_hellman密钥交换协议
 ****************************************************************************************"""

from ecc import ecc_mul, G, G_n
from random import randint


def key_generate():
    k = randint(2, G_n[0])
    pk_self = ecc_mul(G[0], k)
    return k, pk_self

def get_key(point_x, point_y, k):
    point = (int(point_x), int(point_y))
    return ecc_mul(point, k)

if(__name__ == '__main__'):
    print("1")


