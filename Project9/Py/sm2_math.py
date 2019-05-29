"""****************************************************************************************
 ** FileName:       sm2_math.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-18 星期六 15:35:08
 ** Description:    实现SM2所需要的一些基础函数
                    字节串用16进制表示即可
 ****************************************************************************************"""
from ecc import p, p_len, Infin


def int2bytes_string(x, k):             # k为输出字节长度，x为要转换的整数
    if(2 ** (8 * k) <= x):
        print('Error! 2 ^ (8k) should > x')
        exit()
    bytes_string = [None] * k
    for i in range(k - 1, -1, -1):
        bytes_string[i] = (hex(x & 0xff)[2:]).zfill(2)
        x = x >> 8
    return ''.join(bytes_string)


def bytes_string2int(bytes_string):
    res = 0
    l = len(bytes_string) >> 1
    for i in range(l):
        res = (res << 8) + int(bytes_string[i << 1: (i + 1) << 1], 16)
    return res

def bit2bytes_string(s):     #bit串s
    m = len(s)
    k = (m + 7) >> 3
    bytes_string = [None] * k
    for i in range(k):
        if(m < 8):
            bytes_string[i] = (hex(int(s, 2))[2:]).zfill(2)
        else:
            bytes_string[i] = (hex(int(s[:8], 2))[2:]).zfill(2)
            s = s[8:]
        m = m - 8
    return ''.join(bytes_string)



def bytes_string2bit(M):    #字节串m
    k = len(M)
    bit = [None] * (k >> 1)
    for i in range(k >> 1):
        bit[i] = (bin(int(M[i * 1: (i + 1) << 1], 16))[2:]).zfill(8)
    return ''.join(bit)


def field2bytes_string(field):  #Fp域中元素field
    l = (p_len[0] + 7) >> 3
    return int2bytes_string(field, l)

def bytes_string2field(bytes_string):
    return bytes_string2int(bytes_string)


def field2int(field):
    return field



def point2bytes_string(point):    # point为所要转换的点,默认采用不压缩的形式
    if(point == Infin[0]):
        print("Error!point2bytes_string输入不为无穷远点")
        exit()
    else:
        x1 = field2bytes_string(point[0])
        y1 = field2bytes_string(point[1])
        return '04' + x1 + y1

def bytes_string2point(bytes_string):
    bytes_string = bytes_string[2:]
    l = len(bytes_string) >> 1
    return (int(bytes_string[:l], 16), int(bytes_string[l:], 16))


if(__name__ == '__main__'):
    print(bytes_string2bit('ab'))
    