"""****************************************************************************************
 ** FileName:        Attack_Subtitution.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-03-19 星期二 09:55:30
 ** Description:     在无人干预下实现对单表替换密码的字母频率攻击
 ****************************************************************************************"""
import copy

"""****************************************************************************************
 ** Date:            2019-03-19 星期二 09:56:09
 ** Description:     实现简单的单表替换密码
 ****************************************************************************************"""



def single_key(word):
    new_word = copy.deepcopy(word)
    keys = []
    for i in new_word:
        if(i >= 'a' and i <= 'z' and i not in keys):
            keys.append(i)
    for i in range(97, 123):
        if(chr(i) not in keys):
            keys.append(chr(i))
    return keys



def sin_encode(keys, message):
    cipher = []
    index = 0
    length = len(keys)
    for i in message:
        if(index == length):
            index = 0
        cipher.append( keys[ord(i) - 97])
        index = index + 1
    return ''.join(cipher)



def sin_decode(keys, cipher):
    message = []
    index = 0
    length = len(keys)
    for i in cipher:
        if(index == length):
            index = 0
        message.append(chr(keys.index(i) + 97))
    return ''.join(message)



"""****************************************************************************************
 ** Date:            2019-03-19 星期二 10:15:30
 ** Description:     实现对于单表加密算法的字母频率攻击
 ****************************************************************************************"""


def get_fre(cipher, n):                                 #cipher为密文，n为要查询的语言统计学n阶规律，返回数组
    fre = {}
    for i in range(len(cipher) - n + 1):
        if( cipher[i: i + n] in fre):
            fre[cipher[i: i + n]] = fre[cipher[i: i + n]] + 1
        else:
            fre[cipher[i: i + n]] = 1
    fre = sorted(fre.items(), key = lambda x:x[1], reverse = True)
    return [i[0] for i in fre]


def permutation(per, res, a):                                       #返回per中的所有排列变换
    if( len(per) == 1):
        a.append(per[0])
        res.append(a)
        return 
    for i in range(len(per)):
        tmp = copy.deepcopy(per)
        a_tmp = copy.deepcopy(a)
        a_tmp.append(tmp[i])
        tmp[i] = tmp[0]
        permutation(tmp[1:], res, a_tmp)


def sub(cipher, source, change):                          #将cipher中字母列表‘source’替换成字母列表中的‘change’, 并返回替换字符串
    message = []
    for i in cipher:
        message.append(change[source.index(i)])
    return ''.join(message)

    

                                                        #数组分组[0, 1, 4, 9, 11, 20, 22]
def att(cipher, n):                                        #找出出现的字母表，并简化标准频率（sta_frequency)
    sta_frequency = ['e', 't', 'a', 'o', 'i', 'n', 'r', 'h', 's', 'd', 'l', 'c', 'm', 'p', 'u', 'f', 'g', 'w', 'y', 'b', 'k', 'v', 'j', 'x', 'q', 'z']
    divide = [0, 1, 4, 9, 15, 19, 23, 27]
    frequency = get_fre(cipher, 1)
    length = len(frequency)
    sta_fre = []
    tmp = 1
    while( divide[tmp] < length):
        sta_fre.append(sta_frequency[divide[tmp - 1] : divide[tmp]])
        tmp = tmp + 1
    sta_fre.append(sta_frequency[divide[tmp - 1] : length])

    sta_frequency = []
    permutation(sta_fre[tmp - 1], sta_frequency, [])
    for i in range(tmp - 2, -1, -1):                                 #将其拼接成替换流
        tmp = []
        tmp1 = []
        permutation(sta_fre[i], tmp1, [])
        for j in range(len(sta_frequency)):
            for k in tmp1:
                tmp.append(k + sta_frequency[j])
        sta_frequency = tmp

        if( len(sta_frequency) > n):
                a = []
                for j in sta_fre[:i]:
                    a = a + j
                tmp = []
                for i in sta_frequency:
                    tmp.append(sub(cipher, frequency, a + i))
                return tmp
    
    tmp = []
    for i in sta_frequency:
        tmp.append(sub(cipher, frequency, i))
    return tmp

# s = 'the birth of cars have made an enormous change to our life.in the past,we travel from one place to another only by foot,nowaday,cars can do it .its goes withour saying that the invention of cars bring great benefit to all of us.but as proverb goes:no garden without weeds.car is not exception.owing a car has a lot of advantages.for one thing,car provide us the most convient way of transportation.we can get around freely without spenting a lot of time.emotionally,i always found driving is so exciting.for another,its the comfortable to drive a car.In winter.drivers always can stay warm and dry even in rainy whether,in addition,drivers are usually safe in their cars when they are out at night.Cars bring the human merits,their side-effects graudually come to the surface.firstly,to run a car need a lot of oil,which is getting less and less.the increasing number of cars contribute the lacking of energy.secondlly,as  more and more cars are used,the traffic ecpecially in big cities is getting heaver and heavier,which lead to the serious social problem--traffic jam.in addition,the inceasing numbers of cars ,which excaust sent a huge quantities of carbon monoxide into atmosphere.it make the air of cities unbreathabe,it strip people contact with frensh air.therefore,the new energy should be explored to replace the oil so that our envionmental pollution can be avioded .and the strick law should be issued to keep the numbers of cars under control.thus,our heavier traffic can be solluted!'
word = input("请输入单表代替密码的密钥:")
keys = single_key(word)
file_in = open("message.txt", "r")
tmp = file_in.read()
message = ''
while(tmp != ''):
    message = message + tmp
    tmp = file_in.read()

file_in.close()

message = ''.join([i.lower() for i in message if(ord(i.lower()) >= 97 and ord(i.lower()) <= 123)])
cipher = sin_encode(keys, message)
print('单表加密的密文为:{0}'.format(cipher) )
print('原文是:{0}\n通过单表解密的密文为:{1}'.format(message, sin_decode(keys, cipher)) )

n = int(input("请输入想要的输出个数:"))
message_att = att(cipher, n)
print('下面是自动攻击所给出的单表解密：')
if( n > len(message_att) ):
    n = len(message_att)
for i in range(n):
    print('No.{0} 原文：   {1}'.format(i + 1, message_att[i]))
input()
