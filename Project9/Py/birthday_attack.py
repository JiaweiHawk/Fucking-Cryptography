"""****************************************************************************************
 ** FileName:       birthday_attack.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-27 星期一 00:59:52
 ** Description:    实现生日攻击
                    使用SHA-1
 ****************************************************************************************"""
from hashlib import sha1
from sha3 import hash_sha3
from sha3 import Para
from random import randint

def generate(seed1, seed2, number):
    real_message = [None] * number
    fake_message = [None] * number


    for i in range(number):
        tmp = (hex(randint(1, 2 ** seed1))[2:]).zfill(seed1)
        while(tmp in real_message):
            tmp = (hex(randint(1, 2 ** seed1))[2:]).zfill(seed1)
        real_message[i] = tmp

    for i in range(number):
        tmp = (hex(randint(1, 2 ** seed2))[2:]).zfill(seed2)
        while(tmp in fake_message):
            tmp = (hex(randint(1, 2 ** seed2))[2:]).zfill(seed2)
        fake_message[i] = tmp
    return real_message, fake_message


def attack(real_message, fake_message, mode):
    number = 2 ** (mode >> 1)
    dic = [None] * number
    for i in range(number):
        dic[i] = hash_sha3(bytes.fromhex(real_message[i]), mode)
    
    for i in range(number):
        Hash_1 = sha1() #
        Hash_1.update(bytes.fromhex(fake_message[i])) #
        tmp = hash_sha3(bytes.fromhex(fake_message[i]), mode)
        if(tmp in dic):
            return (real_message[dic.index(tmp)], fake_message[i])
    
    return None




if(__name__ == '__main__'):
    mode = 12               # hash函数的输出长度
    length = (mode >> 3) << 3
    Para[mode] = (1600 - length, length)

    real_message, fake_message = generate(4 * mode, 2 * mode, 2 ** (mode >> 1))
    res = attack(real_message, fake_message, mode)
    while(res == None):
        real_message, fake_message = generate(randint(1, 100), randint(1, 100), 2 ** (mode >> 1))
        res = attack(real_message, fake_message, mode)

    print('{0}的hash为{1}'.format(res[0], hash_sha3(bytes.fromhex(res[0]), mode)))
    print('{0}的hash为{1}'.format(res[1], hash_sha3(bytes.fromhex(res[1]), mode)))



# def generate(length):
#     a = [None] * (length)
#     b = [None] * (length)
#     for i in range(length):
#         a[i] = bytes(str(randint(1, length)), encoding = 'utf-8')
    
#     for i in range(length):
#         b[i] = bytes(str(randint(1, length)), encoding = 'utf-8')
    
#     return a, b


# def attack(a, b, number):
#     dic = [None] * number
#     for i in range(number):
#         Hash = sha1()
#         Hash.update(a[i])
#         dic[i] = Hash.hexdigest()
    
#     for i in range(number):
#         Hash = sha1()
#         Hash.update(a[i])
#         tmp = Hash.hexdigest()
#         if(tmp in dic):
#             return (a[a.index(b[i])], b[i])
    
#     return None, None


# if(__name__ == '__main__'):
    
#     length = 2 ** 20
#     real, fake = generate(length)
#     real, fake = attack(real, fake, length)
#     while(real == None):
#         real, fake = generate(length)
#         real, fake = attack(real, fake, length)
    
#     Hash = sha1()
#     Hash.update(real)
#     print('消息:{0}的Hash值为{1}'.format(real.decode(encoding = 'utf-8'), Hash.hexdigest()))

#     Hash = sha1()
#     Hash.update(fake)
#     print('消息:{0}的Hash值为{1}'.format(fake.decode(encoding = 'utf-8'), Hash.hexdigest()))