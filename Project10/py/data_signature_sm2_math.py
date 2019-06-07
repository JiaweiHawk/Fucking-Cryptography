"""****************************************************************************************
 ** FileName:       data_signature_sm2_math.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-18 星期六 15:35:08
 ** Description:    实现SM2所需要的一些基础函数
                    字节串用16进制表示即可
 ****************************************************************************************"""
from ecc import p, p_len, Infin, a, b


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

    
def int2bytes_string(x, k):             # k为输出字节长度，x为要转换的整数
    if(2 ** (8 * k) <= x):
        print('Error! 2 ^ (8k) should > x')
        exit()
    bytes_string = [None] * k
    for i in range(k - 1, -1, -1):
        bytes_string[i] = (hex(x & 0xff)[2:]).zfill(2)
        x = x >> 8
    return ''.join(bytes_string)


def bytes_string2int(bytes_string):
    res = 0
    l = len(bytes_string) >> 1
    for i in range(l):
        res = (res << 8) + int(bytes_string[i << 1: (i + 1) << 1], 16)
    return res

def bit2bytes_string(s):     #bit串s
    m = len(s)
    k = (m + 7) >> 3
    bytes_string = [None] * k
    for i in range(k):
        if(m < 8):
            bytes_string[i] = (hex(int(s, 2))[2:]).zfill(2)
        else:
            bytes_string[i] = (hex(int(s[:8], 2))[2:]).zfill(2)
            s = s[8:]
        m = m - 8
    return ''.join(bytes_string)



def bytes_string2bit(M):    #字节串m
    k = len(M)
    bit = [None] * (k >> 1)
    for i in range(k >> 1):
        bit[i] = (bin(int(M[i << 1: (i + 1) << 1], 16))[2:]).zfill(8)
    return ''.join(bit)


def field2bytes_string(field):  #Fp域中元素field
    l = (p_len[0] + 7) >> 3
    return int2bytes_string(field, l)

def bytes_string2field(bytes_string):
    return bytes_string2int(bytes_string)


def field2int(field):
    return field



def qexp(exp, n, mod):
    if( exp < 2):
        return exp
    else:
        base = exp
        ans = 1
        while (n > 0):
            if (n & 1 == 1):
                ans = (ans * base) % mod
            base = (base * base) % mod
            n = n >> 1
        return ans



def sqrt_g(g):  #获取 g mod q 的平方根
    u = (p[0] - 3) >> 2
    y = qexp(g, u + 1, p[0])
    if( ((y * y) % p[0]) == g):
        return y
    else:
        print('Error!have no sqrt')
        exit()



def point2bytes_string(point):    # point为所要转换的点,默认采用压缩形式
    if(point == Infin[0]):
        print("Error!point2bytes_string输入不为无穷远点")
        exit()
    else:
        yp_ = point[1] & 0x1
        x1 = field2bytes_string(point[0])
        if(yp_ == 0):
            return '02' + x1
        else:
            return '03' + x1

    
def bytes_string2point(bytes_string):
    pc = bytes_string[:2]
    x1 = int(bytes_string[2:], 16)
    if(pc != '02' and pc != '03'):
        print('Error!bytes_string2point error')
        exit()
    a_1 = (x1 ** 3 + a[0] * x1 + b[0]) % p[0]


    if(pc == '02'):
        y1 = sqrt_g(a_1)
        if(y1 & 0x1 == 0):
            return (x1, y1)
        else:
            return (x1, p[0] - y1)
        
    else:
        y1 = sqrt_g(a_1)
        if(y1 & 0x1 == 1):
            return (x1, y1)
        else:
            return (x1, p[0] - y1)


if(__name__ == '__main__'):
    print('1')