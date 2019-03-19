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

sta_frequency = [['e'], ['t', 'a', 'o'], ['i', 'n', 's', 'h', 'r'], ['d', 'l'], ['c', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'u'], ['v', 'k'], ['j', 'x', 'q', 'x']]

sta_double_frequency = ['th', 'he', 'in']


def get_fre(cipher, n):                                 #cipher为密文，n为要查询的语言统计学n阶规律，返回字典
    fre = {}
    for i in range(len(cipher) - n):
        if( cipher[i: i + n] in fre):
            fre[cipher[i: i + n]] = fre[cipher[i: i + n]] + 1
        else:
            fre[cipher[i: i + n]] = 1
    fre = sorted(fre.items(), key = lambda x:x[1], reverse = True)
    return [i[0] for i in fre]



def get_fre_doublesame(cipher):                         #cipher为密文，返回叠词的频率
    fre = {}
    for i in range(len(cipher) - 1):
        if(cipher[i] == cipher[i + 1]):
            if(cipher[i: i + 2] in fre):
                fre[cipher[i: i + 2]] = fre[cipher[i: i + 2]] + 1
            else:
                fre[cipher[i: i + 2]] = 1
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
    res = []
    tmp = []
    message = []
    permutation(source, res, [])
    for i in res:
        tmp = []
        for j in cipher:
            if(j in source):
                tmp.append(change[i.index(j)])
            else:
                tmp.append(j)
        message.append(''.join(tmp))
    return message


def att(cipher):
    fre = {}
    message = []
    alpha = list(set(cipher))
    




# word = input("请输入单表代替密码的密钥:")
# keys = single_key(word)
# message = input("请输入明文")
# cipher = sin_encode(keys, message)
# print('单表加密的密文为:{0}'.format(cipher) )
# print('原文是:{0}\n通过单表解密的密文为:{1}'.format(message, sin_decode(keys, cipher)) )
