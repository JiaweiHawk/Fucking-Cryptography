"""****************************************************************************************
 ** FileName:       ecc.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-15 星期三 19:11:26
 ** Description:    实现椭圆曲线上的一些运算
 ****************************************************************************************"""

from copy import deepcopy



def euc_ext(a, b):                      #Euclid扩展算法
    if( b == 0):
        return (1, 0)
    x_pre = 1
    x = 0
    y_pre = 0
    y = 1
    q = int( a // b)
    tmp = a - q * b
    while( tmp != 0):
        a = b
        b = tmp

        tmp = x_pre - q * x
        x_pre = x
        x = tmp

        tmp = y_pre - q * y
        y_pre = y
        y = tmp

        q = int(a // b)
        tmp = a - q * b
    return (x, y)

"""****************************************************************************************
 ** Date:           2019-05-15 星期三 19:11:26
 ** Description:    我们将椭圆曲线选为Zp上的椭圆曲线
                    y^2 = x^3 + ax + b
                    p = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF
                    a = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFC
                    b = 28E9FA9E 9D9F5E34 4D5A9E4B CF6509A7 F39789F5 15AB8F92 DDBCBD41 4D940E93 
                    n = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF 7203DF6B 21C6052B 53BBF409 39D54123 
                    g_x = 32C4AE2C 1F198119 5F990446 6A39C994 8FE30BBF F2660BE1 715A4589 334C74C7 
                    g_y = BC3736A2 F4F6779C 59BDCEE3 6B692153 D0A9877C C62A4740 02DF32E5 2139F0A0
                    G为生成元， G = (g_x, g_y)
                    而G_n是G的阶
 ****************************************************************************************"""

p_len = [256]
p = [0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF]
a = [0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC]
b = [0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93] 
G_n = [0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123]  #   G的阶
G_x = [0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7] 
G_y = [0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0]
G = [(G_x[0], G_y[0])]

Infin = [("无穷远", "无穷远")]


"""****************************************************************************************
 ** Date:           2019-05-15 星期三 19:30:12
 ** Description:    ecc上的加法
                    若是倍加，则仅仅需要输入的point_a == point_b即可
 ****************************************************************************************"""


def ecc_add(point_a, point_b):
    if(point_a == Infin[0]):
        return deepcopy(point_b)
    if(point_b == Infin[0]):
        return deepcopy(point_a)
        
    if(point_a == point_b):
        if(point_a[1] == 0):
            return Infin[0]
        lam = ((point_a[0] * point_a[0] * 3 + a[0]) * (euc_ext(2 * point_a[1], p[0])[0])) % p[0]
    else:
        if(point_a[0] == point_b[0]):
            return Infin[0]
        lam = ((point_b[1] - point_a[1]) * euc_ext(point_b[0] - point_a[0], p[0])[0]) % p[0]

    x = (lam * lam - point_a[0] - point_b[0]) % p[0]
    return (x, (lam * (point_a[0] - x) - point_a[1]) % p[0])


"""****************************************************************************************
 ** Date:           2019-05-15 星期三 19:30:12
 ** Description:    ecc上的数乘
                    根据椭圆曲线群的交换律和结合律
 ****************************************************************************************"""

def ecc_mul(point, k):
    if(k == 0):
        return Infin[0]
    res = None
    while(k > 0):
        if(k & 1 == 1):
            if(res == None):
                res = deepcopy(point)
            else:
                res = ecc_add(res, point)
        point = ecc_add(point, point)
        k = k >> 1
    if(res == None):
        res = point
    return res



if(__name__ == '__main__'):
    print(ecc_mul(G[0], G_n[0]))



