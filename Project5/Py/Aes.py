"""****************************************************************************************
 ** FileName:        Aes.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-04-03 星期三 14:07:15
 ** Description:     实现AES加、解密
 ****************************************************************************************"""

from Aes_math import add_gf, inv_gf, mul_gf, s_box, s_box_inv


"""****************************************************************************************
 ** Date:            2019-04-03 星期三 14:10:32
 ** Description:     实现16进制转2进制、2进制转16进制，自动以0补全位数 全部为字符串，不待标识符0x，0b
 ****************************************************************************************"""

def hex2bin(in_hex):
    length = len(in_hex)
    return (bin(int(in_hex, 16))[2:]).zfill(length * 4)


def bin2hex(in_bin):
    length = len(in_bin)
    return (hex(int(in_bin, 2))[2:]).zfill(length >> 4)



"""****************************************************************************************
 ** Date:            2019-04-03 星期三 15:56:56
 ** Description:     将输入的32位16进制转换为Aes的矩阵流（仍以一位矩阵表示)及其反过程
 ****************************************************************************************"""
def stream2matrix(stream_32):
    stream_32 = stream_32
    res = [0] * 16
    count = 0
    for i in range(4):
        for j in range(4):
            res[4 * j + i] = stream_32[count:count + 2]
            count = count + 2
    return ''.join(res)

def matrix2stream(matrix):
    stream = [0] * 16
    count = 0
    for i in range(4):
        for j in range(4):
            stream[count] = matrix[ (j * 4 + i) * 2 : (j * 4 + i + 1) * 2]
            count = count + 1
    return ''.join(stream)
"""****************************************************************************************
 ** Date:            2019-04-03 星期三 14:08:07
 ** Description:     实现AES的基本部件          所有的输入输出皆使用16进制字符串,不带标识符0x
 ****************************************************************************************"""



"""****************************************************************************************
 ** Date:            2019-04-03 星期三 19:10:54
 ** Description:     字节替换及其逆运算
 ****************************************************************************************"""


def subBytes(in_32):
    res = [0] * 16
    for i in range(16):
        row = int(in_32[2 * i], 16)
        col = int(in_32[2 * i + 1], 16)
        res[i] = s_box[row][col]
    return ''.join(res)


def subBytes_inv(in_32):
    res = [0] * 16
    for i in range(16):
        row = int(in_32[2 * i], 16)
        col = int(in_32[2 * i + 1], 16)
        res[i] = s_box_inv[row][col]
    return ''.join(res)



"""****************************************************************************************
 ** Date:            2019-04-04 星期四 15:28:13
 ** Description:     行变换及其逆变换
 ****************************************************************************************"""


def shitftrow(in_32):
    return in_32[:8] + in_32[10:16] + in_32[8:10] + in_32[20:24] + in_32[16:20] +\
        in_32[30:32] + in_32[24:30]



def shitftrow_inv(in_32):
    return in_32[:8] + in_32[14:16] + in_32[8:14] + in_32[20:24] + in_32[16:20] +\
        in_32[26:32] + in_32[24:26]
    

"""****************************************************************************************
 ** Date:            2019-04-04 星期四 15:46:41
 ** Description:     列混淆及其逆变换
 ****************************************************************************************"""


def mixcolumns(in_32):
    in_16 = [0] * 16
    res = [0] * 16
    for i in range(16):
        in_16[i] = in_32[i * 2:i * 2 + 2]
    
    for col in range(4):
        res[col] = add_gf(mul_gf('02',in_16[col]), add_gf(mul_gf('03', in_16[4 + col]), \
            add_gf(in_16[8 + col], in_16[12 + col])))
        
        res[4 + col] = add_gf(mul_gf('02',in_16[4 + col]), add_gf(mul_gf('03', in_16[8 + col]), \
            add_gf(in_16[col], in_16[12 + col])))
        
        res[8 + col] = add_gf(mul_gf('02',in_16[8 + col]), add_gf(mul_gf('03', in_16[12 + col]), \
            add_gf(in_16[col], in_16[4 + col])))
        
        res[12 + col] = add_gf(mul_gf('02',in_16[12 + col]), add_gf(mul_gf('03', in_16[col]), \
            add_gf(in_16[8 + col], in_16[4 + col])))
    
    return ''.join(res)



def mixcolumns_inv(in_32):
    in_16 = [0] * 16
    res = [0] * 16
    for i in range(16):
        in_16[i] = in_32[i * 2:i * 2 + 2]
    
    for col in range(4):
        res[col] = add_gf(mul_gf('0e',in_16[col]), add_gf(mul_gf('0b', in_16[4 + col]), \
            add_gf(mul_gf('0d',in_16[col + 8]), mul_gf('09',in_16[col + 12]))))
        
        res[col + 4] = add_gf(mul_gf('09',in_16[col]), add_gf(mul_gf('0e', in_16[4 + col]), \
            add_gf(mul_gf('0b',in_16[col + 8]), mul_gf('0d',in_16[col + 12]))))
        
        res[col + 8] = add_gf(mul_gf('0d',in_16[col]), add_gf(mul_gf('09', in_16[4 + col]), \
            add_gf(mul_gf('0e',in_16[col + 8]), mul_gf('0b',in_16[col + 12]))))
        
        res[col + 12] = add_gf(mul_gf('0b',in_16[col]), add_gf(mul_gf('0d', in_16[4 + col]), \
            add_gf(mul_gf('09',in_16[col + 8]), mul_gf('0e',in_16[col + 12]))))
    
    return ''.join(res)



def add_around_key(in_32, key):
    res = [0] * 16
    for i in range(16):
        res[i] = add_gf(in_32[i * 2:i * 2 + 2], key[i * 2:i * 2 + 2])
    return ''.join(res)

"""****************************************************************************************
 ** Date:            2019-04-04 星期四 23:36:21
 ** Description:     密钥生成算法
 ****************************************************************************************"""

rc = [
    '01', '02', '04', '08', '10', '20', '40', '80', '1b', '36'
]


def g(w3, rc):                              #g函数
    w3 = s_box[int(w3[2], 16)][int(w3[3], 16)] + s_box[int(w3[4], 16)][int(w3[5], 16)]\
         + s_box[int(w3[6], 16)][int(w3[7], 16)] + s_box[int(w3[0], 16)][int(w3[1], 16)]
    return add_gf(w3[:2], rc) + w3[2:] 

def w_xor(wa, wb):
    return add_gf(wa[:2], wb[:2]) + add_gf(wa[2:4], wb[2:4]) + add_gf(wa[4:6], wb[4:6])\
     + add_gf(wa[6:8], wb[6:8])


def get_keys(key_32):
    res = [0] * 11
    w0 = key_32[0:2] + key_32[8:10] + key_32[16:18] + key_32[24:26]
    w1 = key_32[2:4] + key_32[10:12] + key_32[18:20] + key_32[26:28]
    w2 = key_32[4:6] + key_32[12:14] + key_32[20:22] + key_32[28:30]
    w3 = key_32[6:8] + key_32[14:16] + key_32[22:24] + key_32[30:32]
    res[0] = key_32
    for i in range(0, 10):
        w0 = w_xor(w0, g(w3, rc[i]))
        w1 = w_xor(w0, w1)
        w2 = w_xor(w2, w1)
        w3 = w_xor(w3, w2)
        tmp = list(w0 + w1 + w2 + w3)
        for row in range(4):
            for col in range(row):
                a = 2 * (row * 4 + col)
                b = 2 * (col * 4 +row)
                tmp1 = tmp[a: a+2]
                tmp[a : a + 2] = tmp[b : b + 2]
                tmp[b:b+2] = tmp1
        res[i + 1] = ''.join(tmp)
    return res

# key = '0f470caf15d9b77f71e8ad67c959d698'
# print(get_keys(key))

def aes_encode(message, key):
    in_16 = [0] * 16
    key_16 = [0] * 16
    for i in range(16):
        in_16[i] = message[i * 2:i * 2 + 2]
        key_16[i] = key[i * 2:i * 2 + 2]
    message = [0] * 16
    key = [0] * 16
    for row in range(4):
        for col in range(4):
            message[row * 4 + col] = in_16[col * 4 + row]
            key[row * 4 + col] = key_16[col * 4 + row]
    message = ''.join(message)
    key = ''.join(key)
    keys = get_keys(key)
    message = add_around_key(message, keys[0])
    for i in range(1, 10):
        message = add_around_key( mixcolumns(shitftrow(subBytes(message))), keys[i])
    # print(shitftrow(subBytes(message)))
    message = add_around_key(shitftrow(subBytes(message)), keys[10])
    message = list(message)
    for row in range(4):
            for col in range(row):
                a = 2 * (row * 4 + col)
                b = 2 * (col * 4 +row)
                tmp1 = message[a: a+2]
                message[a : a + 2] = message[b : b + 2]
                message[b:b+2] = tmp1
    return ''.join(message)


def aes_decode(cipher, key):
    in_16 = [0] * 16
    key_16 = [0] * 16
    for i in range(16):
        in_16[i] = cipher[i * 2:i * 2 + 2]
        key_16[i] = key[i * 2:i * 2 + 2]
    cipher = [0] * 16
    key = [0] * 16
    for row in range(4):
        for col in range(4):
            cipher[row * 4 + col] = in_16[col * 4 + row]
            key[row * 4 + col] = key_16[col * 4 + row]
    cipher = ''.join(cipher)
    key = ''.join(key)
    keys = get_keys(key)
    cipher = add_around_key(cipher, keys[10])
    for i in range(9, 0, -1):
        cipher = add_around_key( mixcolumns_inv(shitftrow_inv(subBytes_inv(cipher))), mixcolumns_inv(keys[i]) )
    cipher = add_around_key(shitftrow_inv(subBytes_inv(cipher)), keys[0])
    message = list(cipher)
    for row in range(4):
            for col in range(row):
                a = 2 * (row * 4 + col)
                b = 2 * (col * 4 +row)
                tmp1 = message[a: a+2]
                message[a : a + 2] = message[b : b + 2]
                message[b:b+2] = tmp1
    return ''.join(message)

if(__name__ =='__main__'):
    message = input('输入明文:')
    key = input('输入密钥:')
    print('\n明文为：{0}\n密钥为：{1}'.format(message, key))
    print('加密的密文是：'+ aes_encode(message, key))
    
    print('')

    cipher = input('输入密文:')
    key = input('输入密钥:')
    print('\n秘文为：{0}\n密钥为：{1}'.format(cipher, key))
    print('解密的明文是：'+aes_decode(cipher, key))
"""****************************************************************************************
 ** Date:            2019-04-03 星期三 16:17:37
 ** Description:     
                     明文：0123456789abcdeffedcba9876543210
                     密钥：0f1571c947d9e8590cb7add6af7f6798
                     密文：ff0b844a0853bf7c6934ab4364148fb9
 ****************************************************************************************"""