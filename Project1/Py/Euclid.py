'''*****************************************************************************************
   ** FileName:        Polynomial.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-12 星期二 21:47:09
   ** Description:     实现生成本原多项式的算法 环上( 在GF(2^n) )
   **************************************************************************************'''
from math import log
import random


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
    m = ( 1 << ( int(n / 2)) )
    for i in range( k, 1 << (n + 1)):
        flag = 1
        for j in range(2, m):
            if( Gf_div(i, j)[1] == 0):
                flag = 0
                break
        if( flag == 1):
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

n = int(input("请输入环上的本原多项式的最高项次数:"))
m = int(input("请输入环上的本原多项式的系数最大值"))
f = int(input("请输入GF(2^n)的n的次数:"))
print('环上的随机生成{0}次本原多项式为：'.format(n, ), end = " ")
for j in pol_r(n + 1, m):
    if( n == 0 or (n > 0 and j != 1) ):
        print('{0}'.format(j), end = "")
    if(n > 1):
        print('x ^ {0} + '.format(n), end = "")
    if( n == 1):
        print('x + '.format(n), end = "")
    n = n - 1
print('\nGF(2^{0})有限域上的所有本原多项式为:'.format(f))
for j in pol_f(f):
    print( bin( j) )

input()
