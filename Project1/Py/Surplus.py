'''*****************************************************************************************
   ** FileName:        Surplus.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 15:22:34
   ** Description:     实现中国剩余定理
   **************************************************************************************'''

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



def surplus_input():                        #实现中国剩余定理的输入
    print("请一行输入一组数，仅包括对应的m(模数)、a(同余数)输入结束后输入q:")
    get = input("请按m a的顺序输入,如果结束所有输入 输入q退出输入:")
    dic = {}
    while( get is not 'q'):
        m, a = map(int, get.split() )
        if( m in dic):
            print("输入错误或无解")
        else:
            dic[m] = a
        get = input("请按m a的顺序输入,如果结束所有输入 输入q退出输入:")
    return dic



def sur_sol(dic):
    if( dic == None):
        return None
    ms = list(dic.keys())
    tmp = ms[0]
    for i in range(1, len(ms) ):
            tmp = tmp * ms[i]
    Ms = [ int(tmp / i) for i in ms]
    ans = 0
    for i in range( len(ms) ):
        (a, b) = euc_ext(Ms[i], ms[i])
        ans = (ans + a * Ms[i] * dic[ms[i]]) % tmp
    return ans



dic = surplus_input()
j = 1
for i in dic.keys():
    print('第{0}个式子: x ≡ {1} (mod {2})'.format(j, dic[i], i))
    j = j + 1
print('由中国剩余定理解得 x = {0}'.format(sur_sol(dic)) )
