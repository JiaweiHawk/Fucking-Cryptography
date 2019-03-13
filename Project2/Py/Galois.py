'''*****************************************************************************************
   ** FileName:        Galois.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-11 星期一 21:42:27
   ** Description:     实现有限域上的四则运算
   ************************************************************************************'''
from math import log

#以0 - 2 ^ n - 1 作为运算的数字



'''*****************************************************************************************
   ** Date:            2019-03-11 星期一 22:02:27
   ** Description:     实现有限域GF(2^4)上的四则运算
   ************************************************************************************'''

m_4 = 0b11001                                       #GF(2^4)上的4次不可约多项式

def mod_4(n):                                       #取模
    while( n > 0b1111):
        n = n ^ (m_4<< (int(log(n, 2)) - 4) )
    return n


def add_4(a, b):                                          #加法
    return mod_4( a ^ b)


def sub_4(a, b):                                         #减法
    return mod_4(a ^ b)


def mul_4(a, b):                                          #乘法
    index = 0
    sum = 0
    while( b != 0):
        if( (b & 1) == 1):
            sum = sum ^ (a << index)
        b = b>>1
        index = index + 1
    return mod_4(sum)

num_4 = [1, 2, 4, 8, 3, 11, 15, 7, 14, 5, 10, 13, 9, 6, 12]                          #生成元，其下表为g^(n - 1)对应的值

def inv_4(b):                                       #计算乘法的逆
    b = mod_4(b)
    if( b == 0):
        return None
    if( b == 1):
        return 1
    return num_4[15 - num_4.index(b)]

def div_4(a, b):  # 除法
    if (b == 0):
        print("Error")
        return
    return mul_4(a, inv_4(b))


'''*****************************************************************************************
   ** Date:            2019-03-11 星期一 22:02:27
   ** Description:     实现有限域GF(2^8)上的四则运算
   ************************************************************************************'''


m_8 = 0b100011011                                      #GF(2^8)上的8次不可约多项式

def mod_8(n):                                       #取模
    while( n > 0b11111111):
        q = int(log(n, 2)) - 8
        n = n ^ (m_8<< q )
    return n


def Gf_div(a, b):                   #求解a(x) / b(x) 即多项式的带余除法
    if( a < b):
        return (0, a)
    if( a == b):
        return (1, 0)
    q = 0
    index = int( log(a, 2)) - int( log(b, 2))
    while( index > 0):
        q =q + (1<<index)
        a = a ^ (b<<index)
        if(a == 0):
            break
        index = int(log(a, 2)) - int(log(b, 2))
    if( a < b):
        return (q, a)
    return (q + 1, a ^ b)



def euc_8(b):
    y_pre = 0
    y = 1
    a = m_8
    q, tmp = Gf_div(a, b)
    while( tmp != 0):
        a = b
        b = tmp

        tmp = y_pre ^ q * y
        y_pre = y
        y = tmp

        q, tmp = Gf_div(a, b)
    return mod_8(y)


def add_8(a, b):                                          #加法
    return mod_8( a ^ b)


def sub_8(a, b):                                         #减法
    return mod_8(a ^ b)


def mul_8(a, b):                                          #乘法
    index = 0
    sum = 0
    while( b != 0):
        if( (b & 1) == 1):
            sum = sum ^ (a << index)
        b = b>>1
        index = index + 1
    return mod_8(sum)

num_8 = [1]
for i in range(2, 2 ** 8):
    num_8.append( mod_8((num_8[i - 2] << 1) ^ num_8[i - 2] ) )

def inv_8(b):                                       #计算乘法的逆
    b = mod_4(b)
    if( b == 0):
        return None
    if( b == 1):
        return 1
    return num_8[255 - num_8.index(b)]

def div_8(a, b):  # 除法
    if( b == 0):
        print("Error")
        return 
    return mul_8(a, inv_8( mod_8(b) ) )


a_4 = int(input("请输入第一个GF(4)的数:"))
b_4 = int(input("请输入第二个GF(4)的数:"))
a_8 = int(input("请输入第一个GF(8)的数:"))
b_8 = int(input("请输入第二个GF(8)的数:"))

print('{0} + {1} = {2}\n{0} * {1} = {3}\n{0} \ {1} = {4}\n{0} - {1} = {5}\n'.format(a_4, b_4, add_4(a_4, b_4), mul_4(a_4, b_4), div_4(a_4, b_4), sub_4(a_4, b_4)))
print('{0} + {1} = {2}\n{0} * {1} = {3}\n{0} \ {1} = {4}\n{0} - {1} = {5}\n'.format(a_8, b_8, add_8(a_8, b_8), mul_8(a_8, b_8), div_8(a_8, b_8), sub_8(a_8, b_8)))
input()