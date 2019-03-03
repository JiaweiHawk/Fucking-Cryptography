'''*****************************************************************************************
   ** FileName:        Surplus.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 15:22:34
   ** Description:     实现中国剩余定理
   **************************************************************************************'''

def gcd(a, b):
    if(a == 0):
        return a
    if(b == 0):
        return b
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp
        tmp = a % b
    return b

def surplus_input():            #实现中国剩余定理的输入
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
        length = len(ms)
        for i in range( length):
            for j in range(i + 1, length):
                if( gcd(ms[i], ms[j]) != 1):
                    self.dic = None
                    return                      #可以将其全部换算为素数
        self.dic = data

    def alg(self):              #进行运算

        ms = list( self.keys() )
        M = []
        for m in ms:
            for



dic = {5:5, 3:3, 4:4}
t1 = surplus(dic)

