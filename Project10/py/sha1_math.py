"""****************************************************************************************
 ** FileName:       sha1_math.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-18 星期六 23:07:41
 ** Description:    实现SHA-1的数学基础
                    函数所有接口为2进制
 ****************************************************************************************"""

packet_len = [512]  #分组长度
register_len = [32]

A = ['01100111010001010010001100000001']
B = ['11101111110011011010101110001001']
C = ['10011000101110101101110011111110']
D = ['00010000001100100101010001110110']
E = ['11000011110100101110000111110000']

K = ['01011010100000100111100110011001', '01101110110110011110101110100001', \
    '10001111000110111011110011011100', '11001010011000101100000111010110']

def add(a, b):
    return  (bin((int(a, 2) + int(b, 2)) & 0xffffffff)[2:]).zfill(register_len[0])

def f1(b, c, d):
    b = int(b, 2)
    c = int(c, 2)
    d = int(d, 2)
    return (bin((b & c) | ((~b) & d))[2:]).zfill(register_len[0])


def f2(b, c, d):
    b = int(b, 2)
    c = int(c, 2)
    d = int(d, 2)
    return (bin(b ^ c ^ d)[2:]).zfill(register_len[0])

def f3(b, c, d):
    b = int(b, 2)
    c = int(c, 2)
    d = int(d, 2)
    return (bin((b & c) | (b & d) | (c & d))[2:]).zfill(register_len[0])



def f4(b, c, d):
    b = int(b, 2)
    c = int(c, 2)
    d = int(d, 2)
    return (bin(b ^ c ^ d)[2:]).zfill(register_len[0])


def lshift(word, number):     #将32bit 2进制循环左移number位
    return word[number:] + word[:number]


def w_generate(packet):        #生成所需要的80个字
    w = [None] * 80
    for i in range(16):
        w[i] = packet[i * 32 : (i + 1) * 32]
    for i in range(16, 80):
        tmp1 = int(w[i - 16], 2)
        tmp2 = int(w[i - 14], 2)
        tmp3 = int(w[i - 8], 2)
        tmp4 = int(w[i - 3], 2)

        w[i] = lshift((bin(tmp1 ^ tmp2 ^ tmp3 ^ tmp4)[2:]).zfill(register_len[0]), 1)
    
    return w


if(__name__ == '__main__'):
    print('1')
    # for b in range(0, 2):
    #     for c in range(0, 2):
    #         for d in range(0, 2):
                # print('{0} {1} {2} {3}'.format(str(b), str(c), str(d), str(f3(str(b), str(c), str(d)))))