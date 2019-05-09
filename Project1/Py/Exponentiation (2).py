'''*****************************************************************************************
   ** FileName:        exponentiation.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 14:39:05
   ** Description:     实现常规模幂算法和快速模幂算法
   **************************************************************************************'''

def nexp(exp, n, mod):                              #常规模幂算法
    ans = 1
    for i in range(n):
        ans = (ans * exp) % mod
    return ans



#快速模幂算法
#算法: exp ^ n mod(m)
#    = (exp ^ 2 mod(m) ) ^ (n/2) mod(m), 当m为偶数
#    = exp * (exp ^ 2 mod(m) ) ^ {(n-1)/2} mod(m), 当m为奇数
#    当n == 0 时结束
def qexp(exp, n, mod):
    if( exp < 2):
        return exp
    else:
        base = exp
        ans = 1
        while (n > 0):
            if (n & 1 == 1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            n = n >> 1
        return ans

e = int(input("请输入底数exp:"))
n = int(input("请输入指数n:"))
m = int(input("请输入底模数mod:"))
n = 2 ** 127 - 2
m = n + 1
print('(Python计算)(exp ^ n) % mod = {0}'.format( (e ** n) % m) )
print('常规模幂算法: (exp ^ n) % mod = {0}'.format(nexp(e, n, m)) )
print('快速幂算法(exp ^ n) % mod = {0}:'.format(qexp(e, n, m)) )
