"""****************************************************************************************
 ** FileName:       knapsack_math.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-08 星期三 16:13:54
 ** Description:    实现背包密码体制及其攻击的数学基础
 ****************************************************************************************"""

from random import randint

"""****************************************************************************************
 ** Date:           2019-05-07 星期二 11:32:51
 ** Description:    欧几里得拓展算法
 ****************************************************************************************"""
def euc_ext(a, b):                     
    if( b == 0):
        return (1, 0, a)
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
    return (x, y, b)
