'''*****************************************************************************************
   ** FileName:        Double_Des_Attack.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-27 星期三 14:43:20
   ** Description:     编写两重s-DES的中间相遇攻击 
   **************************************************************************************'''

import random


'''*****************************************************************************************
   ** Date:            2019-03-27 星期三 14:47:20
   ** Description:     编写s-Des的加密、解密
   **************************************************************************************'''


def xor(a, b):
    res = []
    for i in range( len(a) ):
        res.append( chr( (ord(a[i]) ^ ord(b[i])) + 48) )
    return ''.join(res)



'''*****************************************************************************************
   ** Date:            2019-03-27 星期三 14:47:20
   ** Description:     编写固定的初始置换IP函数, 输入为8bit
   **************************************************************************************'''



ip_sheet = [
    1, 5, 2, 0, 3, 7, 4, 6
    ]


def ip(in_8):

    ans = ['0'] * 8
    for i in range(8):
        ans[i] = in_8[ip_sheet[i]]
    
    return ''.join(ans)



'''*****************************************************************************************
   **************************************************************************************'''

    
def ip_inv(in_8):

    
    ans = ['0'] * 8
    for i in range(8):
        ans[ip_sheet[i]] = in_8[i]

    return ''.join(ans)




'''*****************************************************************************************
   ** Date:            2019-03-20 星期三 14:27:20
   ** Description:     编写加密拓展置换E, 输入为4bit，输出为5bit
   **************************************************************************************'''


E_P_table = [
    3, 0, 1, 2, 1, 2, 3, 0
]

def right_extend(in_4):
    ans = [0] * 8
    for i in range(8):
        ans[i] = in_4[E_P_table[i]]
            
    return ''.join(ans)



table = [
        1, 3, 2, 0   
    ]


def substi_p(in_4):
    
   
    res = [0] * 4
    for i in range(4):
        res[i] = in_4[table[i]]
    
    return ''.join(res)


s =[ 
    [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ],
    [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]
]


def s_box(in_8):
    
    
    res = []
    for i in range(2):
        row = int( (in_8[i * 4] + in_8[i * 4 + 3]), 2)
        col = int( (in_8[i * 4 + 1 : i * 4 + 3]), 2)
        res.append( (bin(s[i][row][col])[2:]).zfill(2))
    return ''.join(res)


'''*****************************************************************************************
   **************************************************************************************'''



'''*****************************************************************************************
   ** Date:            2019-03-27 星期三 15:01:20
   ** Description:     标准密钥处理函数、移位、置换1、置换2
   **************************************************************************************'''


pc1 = [
        2, 4, 1, 6, 3, 9, 0, 8, 7, 5    
    ]


def substi_1(bit_10):

    res = [0] * 10
    for i in range(10):
        res[i] = bit_10[pc1[i]]
    return ''.join(res)


pc2 = [
        5, 2, 6, 3, 7, 4, 9, 8
    ]


def substi_2(bit_10):

    res = [0] * 8
    for i in range(8):
        res[i] = bit_10[pc2[i]]
    return ''.join(res)



shift_table = [
        1, 2
    ]

def get_keys(key_10):
    keys = []

    init = substi_1(key_10)
    left = list(init[:5])
    right = list(init[5:])
    
    for i in range(2):
        for j in range(shift_table[i]):
            tmp = left.pop(0)
            left.append(tmp)

        for j in range(shift_table[i]):
            tmp = right.pop(0)
            right.append(tmp)

        keys.append(substi_2(left +right) )
    
    return keys

def Feistel(in_8, key):
    left = in_8[:4]
    right = in_8[4:]
    right = xor(left, substi_p( s_box(xor(right_extend(right), key)) ))
    return right + in_8[4:]


def sdes_encode(message, keys):
    keys = get_keys(keys)
    cipher = ip(message)
    cipher = Feistel(cipher, keys[0])
    cipher = cipher[4:] + cipher[:4]
    cipher = Feistel(cipher, keys[1])
    return ''.join( (hex(int(ip_inv(cipher), 2))[2:]).zfill(2))


def sdes_decode(cipher, keys):
    cipher = (bin(int(cipher, 16))[2:]).zfill(8)
    keys = get_keys(keys)
    keys.reverse()
    message = ip(cipher)
    message = Feistel(message, keys[0])
    message = message[4:] + message[:4]
    message = Feistel(message, keys[1])
    return ip_inv(message)

"""****************************************************************************************
 ** Date:            2019-03-31 星期天 09:26:09
 ** Description:     实现两重sdes的加解密算法
 ****************************************************************************************"""



def double_des_encode(message, k1, k2):                     #C = E(K2, E(K1,P))
    message = (bin(int(sdes_encode(message,k1), 16))[2:]).zfill(8)
    return sdes_encode(message,k2)

def double_des_decode(cipher, k1, k2):
    cipher = (hex(int(sdes_decode(cipher, k2), 2))[2:]).zfill(2)
    return sdes_decode(cipher, k1)


"""****************************************************************************************
 ** Date:            2019-03-31 星期天 09:53:55
 ** Description:     实现两重sdes的相遇攻击
 ****************************************************************************************"""

def double_des_attack(k1, k2):
    message_known = (bin(random.randint(0, 2 ** 8))[2:]).zfill(8)
    cipher_known = double_des_encode(message_known, k1, k2)
    all_possible_key1 = {}                                          # key:E(k1, message)
    k1_k2_set = []
    for i in range(0, 2 ** 10):
        tmp = (bin(i)[2:]).zfill(10)
        tmp1 = sdes_encode(message_known, tmp)
        if(tmp1 not in all_possible_key1):
            all_possible_key1[tmp1] = []
        all_possible_key1[tmp1].append(tmp)

    for i in range(0, 2 ** 10):
        tmp = (bin(i)[2:]).zfill(10)
        tmp1 = (hex(int(sdes_decode(cipher_known, tmp), 2))[2:]).zfill(2)
        if( tmp1 in all_possible_key1 ):
            for j in all_possible_key1[tmp1]:
                k1_k2_set.append( (j, tmp) )
    
    while( len(k1_k2_set) > 1):
        tmp = []
        message_known = (bin(random.randint(0, 2 ** 8))[2:]).zfill(8)
        cipher_known = double_des_encode(message_known, k1, k2)
        for k1_tmp, k2_tmp in k1_k2_set:
            if( double_des_encode(message_known, k1_tmp, k2_tmp) == cipher_known):
                tmp.append( (k1_tmp, k2_tmp))
        k1_k2_set = tmp

    return (k1_k2_set[0][0], k1_k2_set[0][1])



# # message = input('请输入2位16进制明文:')[2:]     
# message = '0x5e'
# print('明文是：{0}'.format(message))                                     
# message = (bin(int(message, 16))[2:]).zfill(8)                                  
# # keys = input('请输入10位2进制密钥:')[2:]  
# keys = '1010000010'                             
# keys_encode = (bin(int(keys, 2))[2:]).zfill(10)
# print('密钥为：{0}'.format( 'b\'' + keys) )             
# # print("s-DES轮加密")
# cipher = encode(message, keys_encode)                    
# print('最终密文输出为：{0}'.format('0x' + cipher) ) 

# print("")

# cipher = input('请输入2位16进制密文:')[2:]                                  
# keys = input('请输入10位2进制密钥:')[2:]                                
# keys_decode = (bin(int(keys, 2))[2:]).zfill(10)       
# print('密钥为：{0}'.format( 'b\'' + keys) )
# # print("s-Des轮解密")
# message = decode(cipher, keys_decode)                
# print('最终明文输出为：{0}'.format( '0x' + (hex(int(message, 2))[2:]).zfill(2)))
# input()



#-------------------------------------------------------------------------------------#


# message = '0x5e'
# message = (bin(int(message, 16))[2:]).zfill(8)
# k1 = '1010000010'
# k1_encode = (bin(int(k1, 2))[2:]).zfill(10)

# k2 = '0101110001'
# k2_encode = (bin(int(k2, 2))[2:]).zfill(10)

# cipher = double_des_encode(message, k1_encode, k2_encode)
# print(cipher)
# message = double_des_decode(cipher, k1_encode, k2_encode)

# print('0x' + (hex(int(message, 2))[2:]).zfill(2))

# print('0x' + (hex(int(sdes_decode('f1', '1010000010'), 2))[2:]).zfill(2))
k1 = '1010010010'
k2 = '0101010001'
print('待求解的密钥一是：b\'{0}  密钥二是：b\'{1}'.format(k1,k2))
k1_get, k2_get = double_des_attack(k1, k2)
print('结果为——密钥一是：b\'{0}  密钥二是：b\'{1}'.format(k1_get,k2_get))
"""****************************************************************************************
 ** Date:            2019-03-23 星期六 19:54:12
 ** Description:     输入数据
 ****************************************************************************************"""
