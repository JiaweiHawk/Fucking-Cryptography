'''*****************************************************************************************
   ** FileName:        Euclid.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 10:22:38
   ** Date:            2019-03-03 星期日 10:22:38
   ** Description:     Euclid算法、广义Euclid算法、Euclid扩展算法实现
   **************************************************************************************'''

class euclid:

    def __init__(self, a, b):               #初始化
        self.a = a
        self.b = b

    def gcd(self):                          #Euclid算法

        if(self.b == 0):
            return self.a
        if (self.a == 0):
            return self.b

        tmp_a = int(self.a)
        tmp_b = int(self.b)
        tmp = tmp_a % tmp_b

        while( tmp != 0):
            tmp_a = tmp_b
            tmp_b = tmp
            tmp = tmp_a % tmp_b
        return tmp_b


    def general_euclid(self):                       #广义Euclid算法
        r = [int(self.a), int(self.b)]
        q = [0,0]
        r.append(r[0] % r[1])
        index = 2
        while( r[index] != 0):
            index = index + 1
            r.append(r[index - 2] % r[index - 1])
            q.append( int(r[index - 3] / r[index - 2]))

        x = 1                                       #算法:
        y = -q[index - 1]                           #起始:    R(n) = R(n - 2) - q(n) * R(n - 1)
        tmp = 0                                     #转换:   R(n) = x * R(n - 2) + y * R(n - 1)
        for i in range(index - 2, -1, -1):          #            = x * R(n - 2) + y * { R(n - 3) - q(n - 1) * R(n - 2) }
            tmp = x                                 #            = y * R(n - 3) + (x - q(n - 1) * y)
            x = y                                   #终止:    R(n) = x * R(-2)(a) + y * R(-1)(b)
            y = tmp - q[i] * y
        return (x, y)


    def extend_euclid(self):                                #Euclid扩展算法

        if (self.a == 0):                                #gcd(a,b) = x*a + y*b
            return (0, 1)

        if (self.b == 0):
            return (1, 0)

        tmp_a = int(self.a)
        tmp_b = int(self.b)

        q = int(tmp_a / tmp_b)
        tmp = tmp_a % tmp_b
        x_pre = 1
        x = 0
        y_pre = 0
        y = 1
        while( tmp != 0):
            tmp_a = tmp_b                               #r的转移方程
            tmp_b = tmp

            tmp = y_pre - q * y                 #y的转移方程
            y_pre = y
            y = tmp

            tmp = x_pre - q * x                 #x的转移方程
            x_pre = x
            x = tmp

            q = int(tmp_a / tmp_b)
            tmp = tmp_a % tmp_b

        return (x,y)


def gcd(a, b):                      #最终的函数
    if( a == 0):
        return b
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp
        tmp = a % b
    return b

def euc(a, b):                     
    if( b == 0):
        return (0, 1)
    x_pre = 1
    x = 0
    y_pre = 0
    y = 1
    q = int( a / b)
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp

        tmp = x_pre - q * x
        x_pre = x
        x = tmp

        tmp = y_pre - q * y
        y_pre = y
        y = tmp

        q = int(a / b)
        tmp = a % b
    return (x, y)


'''a = int(input("请输入第一个值:"))
b = int(input("请输入第二个值:"))
test = euclid(a, b)
print(test.gcd())
print(test.gcd())
print(test.extension())
(x, y) = test.extension()
print(x * a + y * b)'''
