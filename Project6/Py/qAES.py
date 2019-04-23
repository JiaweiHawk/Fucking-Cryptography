"""****************************************************************************************
 ** FileName:        qAES.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-04-21 星期天 14:47:38
 ** Description:     实现软件AES加解密
                     接口都为state数组
                     通过查表和多线程进行加速
 ****************************************************************************************"""

from qAES_math import s_box, s_box_inv, sheet_gf, shiftrow_table, shiftrow_table_inv, rc
import time    #测试
from multiprocessing import process






def sub_shift(state):
    out = [[None] * 4, [None] * 4, [None] * 4, [None] * 4]
    for row in range(4):
        for col in range(4):
            tmp = shiftrow_table[row][col]
            hang = (state[row][tmp]>>4) & 0xf
            lie = state[row][tmp] & 0xf
            out[row][col] = s_box[hang][lie]
    return out

def col_xor(state, key):
    out = [[None] * 4, [None] * 4, [None] * 4, [None] * 4]
    for col in range(4):
        out[0][col] = sheet_gf[state[0][col]][1] ^ sheet_gf[state[1][col]][2]\
            ^ sheet_gf[state[2][col]][0] ^ sheet_gf[state[3][col]][0] ^ key[0][col]
        out[1][col] = sheet_gf[state[0][col]][0] ^ sheet_gf[state[1][col]][1]\
            ^ sheet_gf[state[2][col]][2] ^ sheet_gf[state[3][col]][0] ^ key[1][col]
        out[2][col] = sheet_gf[state[0][col]][1] ^ sheet_gf[state[1][col]][0]\
            ^ sheet_gf[state[2][col]][1] ^ sheet_gf[state[3][col]][2] ^ key[2][col]
        out[3][col] = sheet_gf[state[0][col]][2] ^ sheet_gf[state[1][col]][0]\
            ^ sheet_gf[state[2][col]][0] ^ sheet_gf[state[3][col]][1] ^ key[3][col]
    return out


def col(state):
    out = [[None] * 4, [None] * 4, [None] * 4, [None] * 4]
    for col in range(4):
        out[0][col] = sheet_gf[state[0][col]][1] ^ sheet_gf[state[1][col]][2]\
            ^ sheet_gf[state[2][col]][0] ^ sheet_gf[state[3][col]][0]
        out[1][col] = sheet_gf[state[0][col]][0] ^ sheet_gf[state[1][col]][1]\
            ^ sheet_gf[state[2][col]][2] ^ sheet_gf[state[3][col]][0]
        out[2][col] = sheet_gf[state[0][col]][0] ^ sheet_gf[state[1][col]][0]\
            ^ sheet_gf[state[2][col]][1] ^ sheet_gf[state[3][col]][2]
        out[3][col] = sheet_gf[state[0][col]][2] ^ sheet_gf[state[1][col]][0]\
            ^ sheet_gf[state[2][col]][0] ^ sheet_gf[state[3][col]][1]
    return out



def xor(state, key):
    out = [[None] * 4, [None] * 4, [None] * 4, [None] * 4]
    for col in range(4):
        out[0][col] = state[0][col] ^ key[0][col]
        out[1][col] = state[1][col] ^ key[1][col]
        out[2][col] = state[2][col] ^ key[2][col]
        out[3][col] = state[3][col] ^ key[3][col]
    return out


def keys_generate(key):
    res = []
    res.append(key)
    for i in range(10):
        hang = (key[1][3]>>4) & 0xf
        lie = key[1][3] & 0xf
        key[0][0] = s_box[hang][lie] ^ rc[i] ^ key[0][0]

        hang = (key[2][3]>>4) & 0xf
        lie = key[2][3] & 0xf
        key[1][0] = s_box[hang][lie] ^ key[1][0]

        hang = (key[3][3]>>4) & 0xf
        lie = key[3][3] & 0xf
        key[2][0] = s_box[hang][lie] ^ key[2][0]

        hang = (key[0][3]>>4) & 0xf
        lie = key[0][3] & 0xf
        key[3][0] = s_box[hang][lie] ^ key[3][0]

        for col in range(1, 4):
            for row in range(4):
                key[row][col] = key[row][col] ^ key[row][col - 1]
        res.append(key)
    return res


def encode(message, key):
    message = xor(message, key[0])
    for i in range(1, 9):
        message = col_xor(sub_shift(message), key[i])
    return xor(sub_shift(message), key[9])


state = [
    [0x01, 0x89, 0xef, 0x67],
    [0x23, 0xab, 0xcd, 0x45],
    [0x45, 0xcd, 0xab, 0x23],
    [0x67, 0xef, 0x89, 0x01]
] 

key = [
    [0x0f, 0x47, 0x0c, 0xaf],
    [0x15, 0xd9, 0xb7, 0x7f],
    [0x71, 0xe8, 0xad, 0x67],
    [0xc9, 0x59, 0xd6, 0x98]
]

#print(keys_generate(key))
# start = time.clock()
print(encode(state, keys_generate(key)))
# print(time.clock()-start)