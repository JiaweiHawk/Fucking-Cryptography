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
        while (n > 1):
            if (n % 2 == 1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            n = int(n / 2)
        return (ans * base) % mod

e = int(input("请输入底数:"))
n = int(input("请输入指数:"))
m = int(input("请输入底模数:"))
print( (e ** n) % m)
print( nexp(e, n, m))
print( qexp(e, n, m))
