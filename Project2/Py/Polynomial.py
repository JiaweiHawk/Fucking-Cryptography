'''*****************************************************************************************
   ** FileName:        Polynomial.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-12 星期二 21:47:09
   ** Description:     实现生成本原多项式的算法 环上( 在GF(2^n) )
   **************************************************************************************'''
from math import log
import random
from copy import deepcopy


def is_poly(i, n): # i 是要检验的二进制表示， n是多项式的次数
    length = len(bin(i)[2:]) - 1

    limit = 1 << length         # 如果大于此值就开始转换
    judge = i - limit
    tmp = deepcopy(judge) << 1
    for j in range(n + 1, (2 ** n) - 1):
        if(tmp > limit):
            tmp = tmp ^ i
        if(tmp == 1):
            return False   
        tmp = tmp << 1

    if(tmp > limit):
        tmp = tmp ^ i
    if(tmp == 1):
        return True
    return False


def gcd(a, b):                      #Euclid算法
    if( a == 0):
        return b
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp
        tmp = a % b
    return b


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


def pol_f(n):
    res = []
    k = ( 1<<n)
    m = ( 1 << ( (n + 1) >> 1) )
    for i in range( k, 1 << (n + 1)):
        flag = 1
        for j in range(2, m):
            if( Gf_div(i, j)[1] == 0):
                flag = 0
                break
        if( flag == 1 and is_poly(i, n)):
            res.append(i)
    return res



def pol_r(n, m):                                      #环上的
    a = []
    for i in range(n):
        a.append( random.randint(1, m))
    if(n == 1):
        return a
    tmp = gcd(a[0], a[1])
    for i in range(2, n):
        tmp = gcd(tmp, a[i])
    for i in range(n):
        a[i] = int(a[i] / tmp)
    return a

n = int(input("请输入环的本原多项式的最高次："))
m = int(input("请输入域的本原多项式的系数最大值："))
f = int(input("请输入有限域GF(2^n)的n值："))
print("环的{0}次本原多项式：".format(n), end = ' ')
for j in pol_r(n + 1, m):
    if( (n > 0 and j != 1) or n == 0):
        print(j, end = '')
    if( n > 1):
        print('x ^ {0} + '.format(n), end = '')
    elif(n == 1):
        print('x + ', end = '')
    n = n - 1
print("\nGF(2^{0})域的{1}个所有本原多项式：".format(f, str(len(pol_f(f)))))
for j in pol_f(f):
    print( bin(j))

input()
