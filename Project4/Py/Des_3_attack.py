"""****************************************************************************************
 ** FileName:        Des_3_attack.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-03-24 星期天 10:12:05
 ** Description:     实现对3轮DES的差分攻击 
 ****************************************************************************************"""



import random
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
   ** Description:     标准密钥处理函数、去掉奇校验、移位、置换1、置换2
   **************************************************************************************'''



pc1 = [
        56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, \
        26, 18, 10, 2, 59, 51, 43, 35, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, \
        37, 29, 21, 13, 5, 60, 52, 44, 36, 28, 20, 12, 4, 27, 19, 11, 3
    ]



def substi_1(bit_64):

    res = [0] * 56
    for i in range(56):
        res[i] = bit_64[pc1[i]]
    return ''.join(res)


pc2 = [
        13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, \
        26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47, 43, 48, \
        38, 55, 33, 52, 45, 41, 49, 35, 28, 31
    ]


def substi_2(bit_56):

    res = [0] * 48
    for i in range(48):
        res[i] = bit_56[pc2[i]]
    return ''.join(res)
    
shift_table = [
        1, 1, 2
    ]

def get_keys(key_64):
    keys = []

    init = substi_1(key_64)

    left = list(init[:28])
    right = list(init[28:])

    
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




table = [
        15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, \
        1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24,
    ]



def substi_p(in_32):

   
    res = [0] * 32
    for i in range(32):
        res[i] = in_32[table[i]]
    
    return ''.join(res)

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

def s_box(in_48):

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
    for i in range(3):
        in_64 = Feistel(in_64, keys[i])
        # print('第{2:>2}轮 | L: {0:<5} | R：{1:<5}'.format((hex(int(in_64[:32], 2))[2:]).zfill(8),\
        # (hex(int(in_64[32:], 2))[2:]).zfill(8), i + 1 ) )          #表达内部的结果
    return in_64


def encode(message, keys):
    keys = get_keys(keys)

    return  Des_3(message, keys)





"""****************************************************************************************
 ** Date:            2019-03-23 星期六 10:00:02
 ** Description:     实现对3轮DES的差分攻击 
 ****************************************************************************************"""

def s_box_attack(in_6, n):
       
    row = int( in_6[0] + in_6[5], 2)
    col = int( (in_6[1 : 5]), 2)
    return (bin(s[n][row][col])[2:]).zfill(4)



def substi_p_inv(in_32):
   
    res = [0] * 32
    for i in range(32):
        res[table[i]] = in_32[i]
    
    return ''.join(res)

def test(e0, e1, c, j):
    res = []
    bxor = xor(e0, e1)
    for i in range(2 ** 6):
        tmp = xor( s_box_attack( (bin(i)[2:]).zfill(6), j), s_box_attack( xor( (bin(i)[2:]).zfill(6), bxor), j))
        if(c[0] == tmp[0] and c[1] == tmp[1] and c[2] == tmp[2] and c[3] == tmp[3]):
            res.append(xor(e0, (bin(i)[2:]).zfill(6)))
    return res



"""****************************************************************************************
 ** Date:            2019-03-23 星期六 10:00:02
 ** Description:     从第三轮k3穷举56位秘钥
 ****************************************************************************************"""


def get_possible_key(key_48):

    num = [8, 17, 21, 24, 34, 37, 42, 53]
    key_56 = [0] * 56
    for i in range(48):
        key_56[pc2[i]] = key_48[i]
    key = []
    permutation = [x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 for x1 in ('0', '1') for x2 in ('0', '1') \
                   for x3 in ('0', '1') for x4 in ('0', '1') for x5 in ('0', '1') for x6 in ('0', '1') \
                   for x7 in ('0', '1') for x8 in ('0', '1')]
    
    for i in range(2 ** 8):
        tmp = copy.deepcopy(key_56)
        for j in range(8):
            tmp[num[j]] = permutation[i][j]
        tmp = ''.join(tmp)
        left = list(tmp[:28])
        right = list(tmp[28:])
        for j in range(2, -1, -1):  
            for k in range(shift_table[j]):
                tmp = left.pop()
                left.insert(0, tmp)
                tmp = right.pop()
                right.insert(0, tmp)
        tmp = ''.join(left + right)
        left = [0] * 64
        for i in range(56):
            left[pc1[i]] = tmp[i]
        tmp = 0
        for i in range(64):
            if(i % 8 == 7):
                left[i] = chr( (tmp - 335) % 2 + 48)        #修改其奇偶校验位       336为偶校验     335为奇校验
                tmp = 0
            else:
                tmp = tmp + ord(left[i])
        key.append(''.join(left))

    return key
        
    
                
            
    

def attack(r, keys):

    l0 = (bin(random.randint(0, 2 ** 32 - 1))[2:]).zfill(32)
    c0 = encode(l0 + r, keys)

    l1 = (bin(random.randint(0, 2 ** 32 - 1))[2:]).zfill(32)
    c1 = encode(l1 + r, keys)

    cxor = substi_p_inv(xor(xor(l0, l1), xor(c0[32:], c1[32:])))
    e0 = right_extend(c0[:32])
    e1 = right_extend(c1[:32])
    res = []
    num = []
    for i in range(8):
        res.append( test(e0[i * 6 : i * 6 + 6], e1[i * 6 : i * 6 + 6], cxor[i * 4 : i * 4 + 4], i))
        num.append(len(res[i]))
    while(num[0] != 1 or num[1] != 1 or num[2] != 1 or num[3] != 1 or num[4] != 1 \
        or num[5] != 1 or num[6] != 1 or num[7] != 1):

        l1 = (bin(random.randint(0, 2 ** 32))[2:]).zfill(32)
        c1 = encode(l1 + r, keys)
        cxor = substi_p_inv(xor(xor(l0, l1), xor(c0[32:], c1[32:])))
        e0 = right_extend(c0[:32])
        e1 = right_extend(c1[:32])

        for i in range(8):
            if( num[i] != 1):
                tmp = test(e0[i * 6 : i * 6 + 6], e1[i * 6 : i * 6 + 6], cxor[i * 4 : i * 4 + 4], i)
                res[i] = [j for j in res[i] if j in tmp]
                num[i] = len(res[i])
    tmp = ''
    for i in res:
        tmp = tmp + ''.join(i)
    res = tmp
    res = get_possible_key(res)

    while( len(res) > 1):
        tmp = []
        m = (bin(random.randint(0, 2 ** 64 - 1))[2:]).zfill(64)
        c = encode(m, keys)
        for i in res:
            if( encode(m, i) == c):
                tmp.append(i)
        res = tmp
    return (hex(int(res[0], 2))[2:]).zfill(16)
    



# message = input('请输入16进制明文:')[2:] 
# message = (bin(int(message, 16))[2:]).zfill(64) 
# keys = input('请输入16进制密钥:')[2:]
# keys_encode = (bin(int(keys, 16))[2:]).zfill(64)
# keys_decode = (bin(int(keys, 16))[2:]).zfill(64)

# cipher = encode(message, keys_encode).zfill(16)
# print('加密的密文为：{0}'.format('0x' + (hex(int(cipher, 2))[2:]).zfill(16)))
# message = (bin(int(message, 16))[2:]).zfill(64)
# print( (bin(0x02468ace ^ 0x13579bdf ^ 0x91998e98 ^ 0xdd2b1751)[2:]).zfill(32))
key_guess = '0x0f1571c947d9e859'
print('待求密钥为：{0}'.format(key_guess))
cipher_odd = attack((bin(int('89ABCDEF', 16))[2:]).zfill(32), (bin(int('0x0f1571c947d9e859', 16))[2:].zfill(64)))
cipher_even = list((bin(int(copy.deepcopy(cipher_odd), 16))[2:]).zfill(64))
for i in range(7, 64, 8):
    #print(cipher_even[i], end = '  ')
    #print((ord(cipher_even[i]) ^ 48))
    cipher_even[i] = chr((ord(cipher_even[i]) ^ 49) + 48)
print('解密的密钥为（采用奇校验）：{0}'.format('0x' + cipher_odd))
print('解密的密钥为（采用偶校验）：{0}'.format('0x' + (hex(int(''.join(cipher_even), 2))[2:]).zfill(16)))
"""****************************************************************************************
 ** Date:            2019-03-23 星期六 19:54:12
 ** Description:     输入3轮加密
                     message: 0x0123456789ABCDEF
                     keys:    0x0f1571c947d9e859
                     cipher:  0x1caaef374cb63528

 ****************************************************************************************"""