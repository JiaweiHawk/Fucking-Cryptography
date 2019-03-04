'''*****************************************************************************************
   ** FileName:        Surplus.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 15:22:34
   ** Description:     实现中国剩余定理
   **************************************************************************************'''
from Euclid import euc_ext                             #使用euc()及gcd()


def surplus_input():                        #实现中国剩余定理的输入
    print("请一行输入一组数，仅包括对应的m(模数)、a(同余数)输入结束后输入q:")
    get = input("输入格式 m  a,结束输入q:")
    dic = {}
    while( get is not 'q'):
        m, a = map(int, get.split() )
        if( m in dic):
            print("输入错误或无解")
        else:
            dic[m] = a
        get = input("输入格式 m  a,结束输入q:")
    return dic



def sur_sol(dic):
    if( dic == None):
        return None
    ms = list(dic.keys())
    Ms = []
    tmp = 1
    for m in ms:
        tmp = tmp * m
        mul = 1
        for other in ms:
            if (other != m):
                mul = mul * other
        Ms.append(mul)
    ans = 0
    for i in range( len(ms) ):
        (a, b) = euc_ext(Ms[i], ms[i])
        ans = (ans + a * Ms[i] * dic[ms[i]]) % tmp
    return ans



dic = surplus_input()
print( sur_sol(dic) )

