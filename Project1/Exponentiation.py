'''*****************************************************************************************
   ** FileName:        exponentiation.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 14:39:05
   ** Description:     实现常规模幂算法和快速模幂算法
   **************************************************************************************'''

class exp:

    def __init__(self, exp, n, m):                  #计算exp ^ n mod(m)
        self.exp = exp
        self.n = n
        self.m = m


    def nexp(self):                                 #常规模幂算法
        ans = 1
        for i in range(self.n):
            ans = (ans * self.exp) % self.m
        return ans

    def qexp(self):                                 #快速模幂算法
        if(self.exp < 2):                           #算法: exp ^ n mod(m)
            return self.exp                         #    = (exp ^ 2 mod(m) ) ^ (n/2) mod(m), 当m为偶数
        tmp_n = int(self.n)                         #    = exp * (exp ^ 2 mod(m) ) ^ {(n-1)/2} mod(m), 当m为奇数
        base = int(self.exp)                        #    当n == 0 时结束
        ans = 1
        while( tmp_n > 1):
            if( tmp_n % 2 == 1):
                 ans = (ans * base) % self.m
            base = (base * base) % self.m
            tmp_n = int(tmp_n / 2)
        return (ans * base) % self.m



e = int(input("请输入底数:"))
n = int(input("请输入指数:"))
m = int(input("请输入底模数:"))
t1 = exp(e,n,10000000000000000000000000000000000000000)
t2 = exp(e, n, m)
print(t1.nexp())
print(t1.nexp() % m)
print(t2.qexp())
