'''*****************************************************************************************
   ** FileName:        Surplus.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 15:22:34
   ** Description:     实现中国剩余定理
   **************************************************************************************'''
import Euclid                               #使用euc()及gcd()


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


class surplus:                  #实现中国剩余定理

    def __init__(self, data):   #进行初始化,其中x ≡ a(i) (mod m(i) )   data为字典 data = {m(i) : a(i)}
        ms = list( data.keys() )
        self.length = len(ms)
        self.mod = 1
        for i in range( self.length):
            self.mod = self.mod * ms[i]
            for j in range(i + 1, self.length):
                if( Euclid.gcd(ms[i], ms[j]) != 1):
                    self.dic = None
                    return                      #可以将其全部换算为素数
        self.dic = data

    def alg(self):              #进行运算
        if( self.dic == None):
            return None
        ms = list( self.dic.keys() )
        M = []
        for m in ms:
            mul = 1
            for other in ms:
                if( other != m):
                    mul = mul * other
            M.append(mul)
        ans = 0
        for i in range( self.length):
            (a, b) = Euclid.euc(M[i], ms[i])
            ans = (ans + a * M[i] * self.dic[ms[i]]) % self.mod

        return ans





dic = {8:3, 3:1, 5:1}
t1 = surplus(dic)
print(t1.alg())

