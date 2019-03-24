"""****************************************************************************************
 ** FileName:        Des_3_attack.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-03-24 星期天 10:12:05
 ** Description:     实现对3轮DES的差分攻击 
 ****************************************************************************************"""




import copy


'''*****************************************************************************************
   ** Date:            2019-03-20 星期三 14:40:20
   ** Description:     标准数据处理函数
   **************************************************************************************'''


def xor(a, b):
    res = []
    for i in range( len(a) ):
        res.append( chr( (ord(a[i]) ^ ord(b[i])) + 48) )
    return ''.join(res)


'''*****************************************************************************************
   **************************************************************************************'''



'''*****************************************************************************************
   ** Date:            2019-03-20 星期三 15:01:20
   ** Description:     标准密钥处理函数增加奇校验、去掉奇校验、移位、置换1、置换2
   **************************************************************************************'''


def addcheck_odd(bit_56):
    res = []
    tmp = 0
    for i in range(56):
        tmp = tmp + ord(bit_56[i])
        res.append(bit_56[i])
        if(i % 7 == 6):
            res.append( chr( (tmp - 336) % 2 + 48) )
            tmp = 0
    return ''.join(res)


def substi_1(bit_64):

    pc1 = [
        56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, \
        26, 18, 10, 2, 59, 51, 43, 35, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, \
        37, 29, 21, 13, 5, 60, 52, 44, 36, 28, 20, 12, 4, 27, 19, 11, 3
    ]

    res = [0] * 56
    for i in range(56):
        res[i] = bit_64[pc1[i]]
    return ''.join(res)


def substi_2(bit_56):

    pc2 = [
        13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, \
        26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47, 43, 48, \
        38, 55, 33, 52, 45, 41, 49, 35, 28, 31
    ]

    res = [0] * 48
    for i in range(48):
        res[i] = bit_56[pc2[i]]
    return ''.join(res)


def get_keys(key_64):
    keys = []

    init = substi_1(key_64)
    left = list(init[:28])
    right = list(init[28:])

    shift_table = [
        1, 1, 2
    ]
    
    for i in range(3):
        for j in range(shift_table[i]):
            tmp = left.pop(0)
            left.append(tmp)

        for j in range(shift_table[i]):
            tmp = right.pop(0)
            right.append(tmp)

        keys.append(substi_2(left +right) )
    
    return keys


'''*****************************************************************************************
   **************************************************************************************'''


'''*****************************************************************************************
   ** Date:            2019-03-20 星期三 15:01:20
   ** Description:     DES模块处理
   **************************************************************************************'''



    
'''*****************************************************************************************
   ** Date:            2019-03-20 星期三 14:27:20
   ** Description:     编写固定的初始置换IP函数, 输入为64bit 输出为 32bit left, 32bit right
   **************************************************************************************'''


def ip(in_64):
    ip_sheet = [
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, \
    13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, \
    26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6
    ]

    ans = ['0'] * 64
    for i in range(64):
        ans[i] = in_64[ip_sheet[i]]
    
    return ''.join(ans)



'''*****************************************************************************************
   **************************************************************************************'''

    
def ip_inv(in_64):

    ip_sheet = [
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, \
    13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, \
    26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6
    ]
    
    ans = ['0'] * 64
    for i in range(64):
        ans[ip_sheet[i]] = in_64[i]

    return ''.join(ans)




'''*****************************************************************************************
   ** Date:            2019-03-20 星期三 14:27:20
   ** Description:     编写加密拓展置换E, 输入为32bit，输出为48bit
   **************************************************************************************'''


def right_extend(in_32):
    ans = []
    for i in range(32):
        if(i % 4 == 0):
            ans.append(in_32[(i - 1)%32])
            
        ans.append(in_32[i])
        
        if(i % 4 == 3):
            ans.append(in_32[(i + 1)%32])
            
    return ''.join(ans)

def substi_p(in_32):
    
    table = [
        15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, \
        1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24,
    ]
   
    res = [0] * 32
    for i in range(32):
        res[i] = in_32[table[i]]
    
    return ''.join(res)



def s_box(in_48):

    s =[ 
        [
            [ 14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, ],
            [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, ],
            [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, ],
            [ 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13, ],
        ],
        [
            [ 15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, ],
            [ 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, ],
            [ 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, ],
            [ 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9, ],
        ],
        [
            [ 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, ],
            [ 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, ],
            [ 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, ],
            [ 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12, ],
        ],
        [
            [ 7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, ],
            [ 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9, ],
            [ 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, ],
            [ 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14, ],
        ],
        [
            [ 2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, ],
            [ 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, ],
            [ 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, ],
            [ 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3, ],
        ],
        [
            [ 12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, ],
            [ 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, ],
            [ 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, ],
            [ 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13, ],
        ],
        [
            [ 4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, ],
            [ 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, ],
            [ 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, ],
            [ 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12, ],
        ],
        [
            [ 13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, ],
            [ 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2, ],
            [ 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, ],
            [ 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11, ],
        ]
    ]
    
    
    res = []
    for i in range(8):
        row = int( (in_48[i * 6] + in_48[i * 6 + 5]), 2)
        col = int( (in_48[i * 6 + 1 : i * 6 + 5]), 2)
        res.append( (bin(s[i][row][col])[2:]).zfill(4))
    return ''.join(res)



"""****************************************************************************************
 ** Date:            2019-03-23 星期六 10:00:02
 ** Description:     一轮迭代加密
 ****************************************************************************************"""

def Feistel(in_64, key):
    left = in_64[:32]
    right = in_64[32:]
    right = xor(left, substi_p( s_box(xor(right_extend(right), key)) ))
    return in_64[32:] + right


"""****************************************************************************************
 ** Date:            2019-03-23 星期六 10:00:02
 ** Description:     3轮迭代加密
 ****************************************************************************************"""

def Des_3(in_64, keys):
    in_64 = ip(in_64)
    print('第IP轮 | L: {0:<5} | R：{1:<5}'.format((hex(int(in_64[:32], 2))[2:]).zfill(8),\
         (hex(int(in_64[32:], 2))[2:]).zfill(8) ) )          #表达内部的结果
    for i in range(3):
        in_64 = Feistel(in_64, keys[i])
        print('第{2:>2}轮 | L: {0:<5} | R：{1:<5}'.format((hex(int(in_64[:32], 2))[2:]).zfill(8),\
        (hex(int(in_64[32:], 2))[2:]).zfill(8), i + 1 ) )          #表达内部的结果
    
    in_64 = in_64[32:] + in_64[:32]

    print('输出   | L: {0:<5} | R：{1:<5}'.format((hex(int(ip_inv(in_64)[:32], 2))[2:]).zfill(8),\
         (hex(int(ip_inv(in_64)[32:], 2))[2:]).zfill(8)) )          #表达内部的结果
    return ip_inv(in_64)


def encode(message, keys):
    keys = get_keys(keys)

    return  hex(int(Des_3(message, keys), 2))[2:]


def decode(cipher, keys):
    cipher = (bin(int(cipher, 16))[2:]).zfill( 64)
    keys = get_keys(keys)
    keys.reverse()
    return hex(int(Des_3(cipher, keys), 2))[2:]


message = input('请输入16进制明文:')[2:] 
message = (bin(int(message, 16))[2:]).zfill(64) 
keys = input('请输入16进制密钥:')[2:]
keys_encode = (bin(int(keys, 16))[2:]).zfill(64)
keys_decode = (bin(int(keys, 16))[2:]).zfill(64)

cipher = encode(message, keys_encode).zfill(16)
print( cipher )
print(decode(cipher, keys_decode))