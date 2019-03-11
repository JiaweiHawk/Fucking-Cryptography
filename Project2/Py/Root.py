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



def factor(n):                       #获取n的所有因子
    if( n < 2):
        return []
    res = []
    j = -1
    for i in range(2, int( n ** 0.5) + 1 ):
        while( n % i == 0):
            if( i in res):
                res.append(res[j] * i)
            else:
                for k in range(j + 1):
                    res.append( res[k] * i)
                    j = j + 1
                res.append(i)
            j = j + 1
            n = int(n / i)

    if( n > 1):
        res.append(n)
    return sorted(res)



def euler(n):                                   #φ(n)
    prime = primes(n)
    sum = 1
    for i in prime:
        sum = sum * (i - 1)
    return sum





def rank(a, n):                            #计算a在n的下的阶Rank(a, n)
    prime = factor(n - 1)
    for i in prime:
        if(qexp(a, i, n) == 1):
            return i
    return euler(n)





def root(n):                                #计算n的一个本原根
    eul = euler(n)
    for i in range(2, n):
        if( rank(i, n) == eul):
            return i
    return None