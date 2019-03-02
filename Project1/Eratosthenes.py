'''*****************************************************************************************
   ** FileName:        Eratosthenes.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-02 星期六 18:01:46
   ** Description:     实现Eratosthenes筛法
   **************************************************************************************'''

import datetime                             #测试

const = 10000000

class io:

    def __init__(self, num, init):          #以init的值初始化[init]*num
        self.num = num
        if( num < const):
            self.table = [init] * num
        else:
            self.table = [init] * num
            self.fil


def eratosthenes( n ):                      #埃氏筛法 筛 1 - n 中所有素数
    if( n < 2):
        return []
    elif( n == 2 ):
        return [2]
    else:
        table = [1] * ( n + 1)
        table[0] = 0
        table[1] = 0

        primes = eratosthenes( int(n ** 0.5) )
        for prime in primes:
            for j in range(prime, int(n / prime) + 1):
                table[prime * j] = 0
        return [x for x in range(2, n + 1) if table[x] == 1]


def eratosthenes_improve( n ):             #埃氏改进筛法 筛 1 - n 中所有素数
    table = [1] * (n + 1)
    for i in range(2, int( n ** 0.5)):
        if( table[i] == 1):
            for j in range(i, int(n / i) + 1):
                table[i * j] = 0
    return [x for x in range(2, n + 1) if table[x] == 1]


def eratosthenes_euler( n ):              #埃氏筛法(欧拉筛) 筛 1 - n 中所有素数
    primes = []
    table = [1] * (n + 1)
    count = 0
    for i in range(2, n + 1):
        if( table[i] == 1):
            primes.append(i)
        for j in primes:
            if( i * j > n):
                break
            table[i * j] = 0        #此处确保每一位数被遍历,如果与判断交换位置会出错,E.X.: 8最终为1
            if( i % j == 0):        #此处确保如果如果一个数被筛到,一定仅仅被筛掉一次而不重复.
                break                       #理由：若n = p1 * p2 * p3 * ...... * pn(素因数按大小顺序排列)
    return  primes                #如果 n <= p1 * p1, 则n 要么为素数，要么n= p1 * p1, 都在i = p1时被筛
                                            #否则就在 i = p2 时被筛
                                            #但易知，其仅被筛一次

num = int(input())
start = datetime.datetime.now()
c = eratosthenes_improve(num)
end = datetime.datetime.now()
#print( (end - start).microseconds)
print( (end - start).seconds)

start = datetime.datetime.now()
c = eratosthenes_euler(num)
end = datetime.datetime.now()
#print( (end - start).microseconds)
print( (end - start).seconds)
