"""****************************************************************************************
 ** FileName:       sha1.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-18 星期六 23:10:14
 ** Description:    实现SHA-1
                    所有接口为2进制
 ****************************************************************************************"""
from hashlib import sha1

from sha1_math import A, B, C, D, E, packet_len, K,\
    f1, f2, f3, f4, lshift, w_generate, add, register_len

block_size = [1024]

"""****************************************************************************************
 ** Date:           2019-05-18 星期六 23:11:12
 ** Description:    实现预处理部分
 ****************************************************************************************"""

def pre_deal(message):
    message_length = len(message) & 0xffffffffffffffff
    pad_length = message_length % packet_len[0]
    if(pad_length < 448):
        pad_length = 448 - pad_length
    else:
        pad_length = packet_len[0] + 448 - pad_length
    

    return message + '1' + '0' * (pad_length - 1) + (bin(len(message))[2:]).zfill(64)#这里不确定是不是地位在高

# # test
# def show_in_hex(bin_number):
#     print((hex(int(bin_number, 2))[2:]).zfill(8))

# 一轮轮函数
def round_function(a, b, c, d, e, round, w):     # 从0到79

    if(round < 20):
        f = f1(b, c, d)
    elif(round < 40):
        f = f2(b, c, d)
    elif(round < 60):
        f = f3(b, c, d)
    else:
        f = f4(b, c, d)

    tmp = add(add(add(add(f, e), lshift(a, 5)), w), K[round // 20])

    return tmp, a, lshift(b, 30), c, d


def H_sha1(a, b, c, d, e, word):        #即压缩函数 80轮轮函数
    a_tmp = a
    b_tmp = b
    c_tmp = c
    d_tmp = d
    e_tmp = e
    word = w_generate(word)

    for i in range(80):
        a_tmp, b_tmp, c_tmp, d_tmp, e_tmp = round_function(a_tmp, b_tmp, c_tmp, d_tmp, e_tmp,\
            i, word[i])
    
    return add(a, a_tmp), add(b, b_tmp), add(c, c_tmp), add(d, d_tmp), add(e, e_tmp)


def hash_sha1(message):       # 此处message为bytes类型    为迭代压缩函数
    length = len(message) << 3
    message = (bin(int(message.hex(), 16))[2:]).zfill(length)
    message = pre_deal(message)
    length = len(message)


    a = A[0]
    b = B[0]
    c = C[0]
    d = D[0]
    e = E[0]

    for i in range(0, length, packet_len[0]):
        a, b, c, d, e = H_sha1(a, b, c ,d ,e, message[i : i + packet_len[0]])
    
    return (hex(int(a + b + c + d + e, 2))[2:]).zfill((register_len[0] * 5) >> 2)


if(__name__ == '__main__'):

    file_in = open("message.txt", "rb")
    message = b''
    tmp = file_in.read(block_size[0])
    while( tmp != b''):
        message = message + tmp
        tmp = file_in.read(block_size[0])
    
    file_in.close()
    
    message = message.decode(encoding = 'utf-8')
    print("从message.txt文件中读入的消息为:{0}\n".format(message))
    message = message.encode(encoding = 'utf-8')

    
    print('使用自己编写的SHA-1得到的结果为:{0}\n'.format(hash_sha1(message)))


    Hash = sha1()
    Hash.update(message)
    print('使用hashlib的SHA-1得到的结果为:{0}\n'.format(Hash.hexdigest()))