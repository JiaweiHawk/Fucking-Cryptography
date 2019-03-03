'''*****************************************************************************************
   ** FileName:        Euclid.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 ������ 10:22:38
   ** Date:            2019-03-03 ������ 10:22:38
   ** Description:     Euclid�㷨������Euclid�㷨��Euclid��չ�㷨ʵ��
   **************************************************************************************'''

class euclid:

    def __init__(self, a, b):               #��ʼ��
        self.a = a
        self.b = b

    def gcd(self):                          #Euclid�㷨
        
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

    '''def recur(self, a, b, x, y):                       #����Euclid�㷨
        if( x == 0):
            return (0, 1)
        if( y == 0):
            return (1, 0)'''

    def extension(self):                                #Euclid��չ�㷨

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
            tmp_a = tmp_b                               #r��ת�Ʒ���
            tmp_b = tmp

            tmp = y_pre - q * y                 #y��ת�Ʒ���
            y_pre = y
            y = tmp

            tmp = x_pre - q * x                 #x��ת�Ʒ���
            x_pre = x
            x = tmp

            q = int(tmp_a / tmp_b)
            tmp = tmp_a % tmp_b

        return (x,y)

a = int(input("�������һ��ֵ:"))
b = int(input("������ڶ���ֵ:"))
test = euclid(a, b)
print(test.gcd())
print(test.gcd())
print(test.extension())
(x, y) = test.extension()
print(x * a + y * b)







