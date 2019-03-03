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

    '''def recur(self, a, b, x, y):                       #广义Euclid算法
        if( x == 0):
            return (0, 1)
        if( y == 0):
            return (1, 0)'''

    def extension(self):                                #Euclid扩展算法

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

a = int(input("请输入第一个值:"))
b = int(input("请输入第二个值:"))
test = euclid(a, b)
print(test.gcd())
print(test.gcd())
print(test.extension())
(x, y) = test.extension()
print(x * a + y * b)







