'''*****************************************************************************************
   ** FileName:        Primality.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-07 星期日 17:04:20
   ** Description:     实现三种素性检验
   **************************************************************************************'''


import random                        #生成随机数





'''*****************************************************************************************
   ** Date:            2019-03-07 星期日 17:04:20
   ** Description:     实现Miller-Rabin素性检验算法
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




def miller(n, t):                      #Miller-Rabin素性检验算法
    if (n == 2 or n == 3):
        return True
    if (n % 2 == 0):
        return False
    k = 0
    q = n - 1
    while( q % 2 == 0):
        k = k + 1
        q = int(q / 2)


    for i in range(t):                  #重复t次
        a = random.randint(2, n - 2)
        if( qexp(a, q, n) == 1):
            continue


        mi = qexp(a, q, n)
        flag = 0
        for j in range(k):
            if( mi == (n - 1) ):
                flag = 1
                break
            mi = (mi * mi) % n
        if( flag):
            continue
        return False
    return True


'''*****************************************************************************************
   ** Date:            2019-03-07 星期日 17:45:20
   ** Description:     实现Fermat素性检验算法
   **************************************************************************************'''

def gcd(a, b):                      #Euclid算法
    if( a == 0):
        return b
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp
        tmp = a % b
    return b



def fermat(n, t):                       #Miller-Rabin素性检验算法
    if( n == 2 or n == 3):
        return True
    if( n % 2 == 0):
        return False
    for i in range(t):
        b = random.randint(1, n - 1)
        d = gcd(b, n)
        if( d != 1):
            return False
        if( qexp(b, n - 1, n) != 1):
            return False
    return True



'''*****************************************************************************************
   ** Date:            2019-03-07 星期日 17:45:20
   ** Description:     实现Solovay-Stassen素性检验算法
   **************************************************************************************'''

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

def legendre(b, n):                   #计算legendre符号s=(b/n)           默认n为奇素数
    if( b % n == 0):
        return 0
    if( qexp(b, int( (n - 1) / 2), n) == 1):
        return 1
    return -1



def jacobi(b, n):                                        #计算Jacobi符号s=(b/n) 默认n为正奇数
    prime = primes(n)
    res = 1
    for i in prime:
        res = res * legendre(b, i)
    return res



def solovay(n, t):                            #Solovay-Stassen素性检验算法
    if( n == 2 or n == 3):
        return True
    if( n % 2 == 0):
        return False
    for i in range(t):
        b = random.randint(2, n - 2)
        r = qexp(b, int( (n - 1) / 2), n)
        if( r == (n - 1) ):
            r = -1
        if( r != 1 and r !=-1 and r != jacobi(b, n)):
            return False
    return True


n = int(input("请输入要检测的数：") )
t = int(input("请输入要检测的次数：") )
print('Miller-Rabin素性检验的结果是：{0}'.format(miller(n, t)) )
print('Miller-Rabin素性检验的结果是：{0}'.format(fermat(n, t) ) )
print('Miller-Rabin素性检验的结果是：{0}'.format(solovay(n, t) ))
input()
