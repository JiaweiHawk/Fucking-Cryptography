'''*****************************************************************************************
   ** FileName:        Euclid.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 10:22:38
   ** Date:            2019-03-03 星期日 10:22:38
   ** Description:     Euclid算法、广义Euclid算法、Euclid扩展算法实现
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


#算法:
#起始:    R(n) = R(n - 2) - q(n) * R(n - 1)
#转换:   R(n) = x * R(n - 2) + y * R(n - 1)
#            = x * R(n - 2) + y * { R(n - 3) - q(n - 1) * R(n - 2) }
#            = y * R(n - 3) + (x - q(n - 1) * y)
#终止:    R(n) = x * R(-2)(a) + y * R(-1)(b)

def euc_gen(a, b):                      #广义Euclid算法
    r = [a, b]
    q = [0, 0]
    index = 1
    while (r[index] != 0):
        r.append(r[index -1] % r[index])
        q.append(int(r[index - 1] / r[index]) )
        index = index + 1
    x = 1
    y = -q[index - 1]
    tmp = 0
    for i in range(index - 2, -1, -1):
        tmp = x
        x = y
        y = tmp - q[i] * y
    return (x, y)



def euc_ext(a, b):                      #Euclid扩展算法
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


a = int(input("请输入第一个值:"))
b = int(input("请输入第二个值:"))
print( gcd(a, b))

(x, y) = euc_gen(a, b)
print('{0} * {1} + {2} * {3} = {4}'.format(x, a, y, b, gcd(a, b)) )

(x, y) = euc_gen(a, b)
print('{0} * {1} + {2} * {3} = {4}'.format(x, a, y, b, gcd(a, b)) )
