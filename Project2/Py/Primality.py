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
    b = random.randint(1, n - 1)
    for i in range(t):
        d = gcd(b, n)
        if( d != 1):
            return False
        b = qexp(b, n - 1, n)
    return True
        


'''*****************************************************************************************
   ** Date:            2019-03-07 星期日 17:45:20
   ** Description:     实现Solovay-Stassen素性检验算法
   **************************************************************************************'''



'''n = int(input("请输入要检测的数：") )
t = int(input("请输入要检测的次数：") )
#print('Miller-Rabin素性检验的结果是：{0}'.format(miller(n, t)) )
print('Miller-Rabin素性检验的结果是：{0}'.format( fermat(n, t) ) )'''
for i in range(2, 1555):
    if( fermat(i, i) ):
        print(i)

    
    
