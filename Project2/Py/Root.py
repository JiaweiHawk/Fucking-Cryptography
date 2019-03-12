'''*****************************************************************************************
   ** FileName:        Root.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-11 星期一 22:19:57
   ** Description:     实现本原根生成算法
   **************************************************************************************'''



def qexp(exp, n, mod):                  #之前实现好的快速幂
    if( exp < 2):
        return exp
    else:
        base = exp
        ans = 1
        while (n > 1):
            if (n % 2 == 1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            n = int(n / 2)
        return (ans * base) % mod

def primes(n):                       #获取n的素因数分解
    if( n < 2):
        return []
    res = []
    for i in range(2, int( n ** 0.5) + 1 ):
        while( n % i == 0):
            res.append(i)
            n = int(n / i)

    if( n > 1):
        res.append(n)
    return res






def euler(n):                                   #φ(n)
    prime = primes(n)
    for i in set(prime):
        n = int( n * (i - 1) / i)
    return n





def rank(a, n):                            #计算a在n的下的阶Rank(a, n)
    c = euler(n)
    for i in range(2, c + 1):
        if( gcd(i, c) != 1 and qexp(a, i, n) == 1):
            return i


def gcd(a, b):                      #Euclid算法
    if( a == 0):
        return b
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp
        tmp = a % b
    return b



def root(n):                                #计算n的一个本原根
    eul = euler(n)
    res = []
    fact = [ i for i in range(2, n) if gcd(i, n) == 1]
    for i in fact:
        if( rank(i, n) == eul):
            res.append(i)
    return res

n = int(input("请输入数字n：",))
print('{0}的本源根有：'.format(n), end = '')
for i in root(n):
    print('{0} '.format(i), end = '')
input()