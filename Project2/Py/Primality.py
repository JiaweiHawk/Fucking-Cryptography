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

def qexp(exp, n, mod):                          #之前的快速幂
    if( exp < 2):
        return exp
    else:
        base = exp
        ans = 1
        while (n > 0):
            if (n & 2 == 1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            n = n >> 1
        return ans




def miller(n, t):                      #Miller-Rabin素性检验算法
    if (n == 2 or n == 3):
        return True
    if (n % 2 == 0):
        return False
    k = 0
    q = n - 1
    while( q % 2 == 0):
        k = k + 1
        q = q >> 1


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

def jacobi(b, n):
    if( gcd(b, n) != 1):
            return 0
    tmp = 0
    res = 1
    b = b % n
    while( b & 1 == 0):
        tmp = tmp + 1
        b = b>>1
    if(tmp & 1 == 1 and ( ((n * n - 1)>>3) & 1 == 1) ):
        res = -res
    while( b > 2):
        if( ( (((b - 1) * (n - 1))>>2) & 1 ) == 1):
            res = -res
        tmp = n % b
        n = b
        b = tmp

        tmp = 0                                     #去除所有2
        while( b & 1 == 0):
            tmp = tmp + 1
            b = b>>1

        if(tmp & 1 == 1 and ( (n * n - 1) >> 3) & 1 == 1):
            res = -res
        
        if( gcd(b, n) != 1):
            return 0
    return res


def solovay(n, t):                            #Solovay-Stassen素性检验算法
    if( n == 2 or n == 3):
        return True
    if( n % 2 == 0):
        return False
    for i in range(t):
        b = random.randint(2, n - 2)
        r = qexp(b, (n - 1)>>1, n)
        if( r == (n - 1) ):
            r = -1
        if( r != 1 and r !=-1 and r != jacobi(b, n)):
            return False
    return True


n = int(input("请输入要检测的数：") )
t = int(input("请输入要检测的次数：") )
n = 2 ** 127 - 1
t = 1000
print('Miller-Rabin素性检验的结果是：{0}'.format(miller(n, t)) )
print('Fermat素性检验的结果是：{0}'.format(fermat(n, t) ) )
print('Solovay-Stassen素性检验的结果是：{0}'.format(solovay(n, t) ))
input()
