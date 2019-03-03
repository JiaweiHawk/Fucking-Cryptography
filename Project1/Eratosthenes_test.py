'''*****************************************************************************************
   ** FileName:        Eratosthenes.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-02 ������ 18:01:46
   ** Description:     ʵ��Eratosthenesɸ��
   **************************************************************************************'''

import datetime                             #����
import os
const = 5

class io:
    def __init__(self, num):          #��init��ֵ��ʼ��[init]*num
        self.num = num
        if( num <= const):
            self.table = [1] * num
        else:
            self.table = [1] * const
            if( os.path.exists('eratosthenes.txt') ):
                os.remove('eratosthenes.txt')
            self.file = open('eratosthenes.txt', 'wb+')         #�����ƴ򿪿��Ը����ļ�ָ������
            for i in range(const + 1, num + 1):
                self.file.write( bytes("1", "utf-8") )
                self.file.flush()

    def write(self, place, value):          #�޸� [place- 1] ��������
        if(place <= const):
            self.table[place - 1] = value
        else:
            self.file.seek(place - const - 1, 0)                   #place - const - 1���ļ�ָ��ӿ�ʼ�ƶ���λ��
            self.file.write( bytes(str(value), "utf-8") )
            self.file.flush()

    def read(self, place):                  #��ȡ [place- 1] ��������
        if (place <= const):
            return int( self.table[place - 1])
        else:
            self.file.seek(place - const - 1, 0)
            return int( self.file.read(1) )

    def prime(self):                 #������������
        primes = []
        for i in range(2, self.num + 1):
            if( self.read(i) == 1):
                primes.append(i)

        return primes


    def delete(self):                       #����д�ļ�
        self.file.close()



def eratosthenes( n, primes):                      #����ɸ�� ɸ 1 - n ����������
    if( n < 2):
        return []
    elif( n == 2 ):
        return [2]
    else:
        table = io(n)

        primes = eratosthenes( int(n ** 0.5) )
        for prime in primes:
            for j in range(prime, int(n / prime) + 1):
                table.write(j,0)
        primes = table.prime()
        table.delete()


def eratosthenes_improve( n, primes):             #���ϸĽ�ɸ�� ɸ 1 - n ����������
    table = io(n)
    for i in range(2, int( n ** 0.5)):
        if( table.read(i) == 1):
            for j in range(i, int(n / i) + 1):
                table.write(i * j, 0)
    primes = table.prime()
    print(primes)
    table.delete()


def eratosthenes_euler( n ):              #����ɸ��(ŷ��ɸ) ɸ 1 - n ����������
    primes = []
    table = io(n)
    count = 0
    for i in range(2, n + 1):
        if( table.read(i) == 1):
            primes.append(i)
        for j in primes:
            if( i * j > n):
                break
            table[i * j] = 0        #�˴�ȷ��ÿһλ��������,������жϽ���λ�û����,E.X.: 8����Ϊ1
            if( i % j == 0):        #�˴�ȷ��������һ������ɸ��,һ��������ɸ��һ�ζ����ظ�.
                break                       #���ɣ���n = p1 * p2 * p3 * ...... * pn(����������С˳������)
    return  primes                #��� n <= p1 * p1, ��n ҪôΪ������Ҫôn= p1 * p1, ����i = p1ʱ��ɸ
                                            #������� i = p2 ʱ��ɸ
                                            #����֪�������ɸһ��

num = int(input())
'''#start = datetime.datetime.now()
c = eratosthenes_improve(num)
end = datetime.datetime.now()
#print( (end - start).microseconds)
print( (end - start).seconds)

start = datetime.datetime.now()
c = eratosthenes_euler(num)
end = datetime.datetime.now()
#print( (end - start).microseconds)
print( (end - start).seconds)'''
primes = []
eratosthenes_improve(num, primes)
print(primes)
