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


def pol(n, m):                                      #环上的
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


