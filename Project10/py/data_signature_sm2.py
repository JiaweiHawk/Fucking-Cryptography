"""****************************************************************************************
 ** FileName:       data_signature_sm2.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-30 星期四 16:14:55
 ** Description:    实现SM2的数字签名算法
                    其所有接口若无特殊说明
                    皆为16进制
 ****************************************************************************************"""

from sha1 import hash_sha1
from sha3 import hash_sha3
from data_signature_sm2_math import bit2bytes_string, bytes_string2bit, point2bytes_string, \
    field2bytes_string, bytes_string2point, bytes_string2int, int2bytes_string,\
    euc_ext
from ecc import ecc_mul, G, p, p_len, G_n, ecc_add, Infin
from random import randint
import threading

v = [160, 256]         #v[0]指密钥杂凑算法的输出bit数，v[1]表示加密时的Hash函数输出bit数


"""****************************************************************************************
 ** Date:           2019-05-18 星期六 14:55:34
 ** Description:    加密方的组件
                    包括KDF算法（其中hash函数选择Sha1()，可以随意修改成其他的)
                    读取公钥。
 ****************************************************************************************"""

def key_generate():
    while(True):
        d = randint(1, G_n[0] - 2)
        pk = ecc_mul(G[0], d)
        if(pk == Infin[0]):
            continue
        return d, pk
    return None
    




# 一些没有必要的过程进行简化, 部分过程标准文档过于麻烦则简化了
# za为关于用户 A 的可辨别标识、部分椭圆曲线系统参数和用户 A 公钥的杂凑值
# k为用户A随机选择的点
# da用户A的私钥。 
def signature(message, za, k, da): # 签名算法， 对消息进行签名 
    message = za + message
    
    e = bytes_string2int(hash_sha3(bytes.fromhex(message), v[1]))

    pa = ecc_mul(G[0], k)

    x1 = pa[0]              # 此步骤为转化pa的点为整形

    r = (e + x1) % G_n[0]
    if(r == 0 or (r + k) == G_n[0]):
        return None
    
    s = (euc_ext(1 + da, G_n[0])[0] * (k - r * da)) % G_n[0]

    if(s == 0):
        return None

    return (field2bytes_string(r), field2bytes_string(s))

"""****************************************************************************************
 ** FileName:       data_signature_sm2.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-06-06 星期四 15:57:57
 ** Description:    签名方函数
 ****************************************************************************************"""

def signatureor(sem):
    print("---------------签名方准备开始签名------------------\n")
    file_in = open("message.txt", "r", encoding = 'utf-8')
    message = ''
    tmp = file_in.readline()
    while(tmp != '消息\n'):
        tmp = file_in.readline()
    tmp = file_in.readline()
    while(tmp != '\n'):
        message = message + tmp
        tmp = file_in.readline()
    file_in.close()
    print("从文件message.txt中读取的内容为：{0}\n".format(message))
    message = bytes(message, encoding = 'utf-8').hex()
    print("消息摘要的16进制表示为:{0}".format(message))
    
    da, pk = key_generate()
    print("生成密钥完毕, 私钥为{0}, 公钥为{1}".format(str(da), str(pk)))
    file_in = open("signature.key", "w", encoding = 'utf-8')
    file_in.write("公钥部分\n{0}\n".format(str(pk[0]) + ' ' + str(pk[1])))
    # 方便起见， 让entla为8的倍数
    entla = (randint(1, (1 << 16) - 1) >> 3) << 3
    ida = (bin(randint(1, 1 << entla))[2:]).zfill(entla)
    za = (bin(entla)[2:]).zfill(16) + ida + bytes_string2bit(field2bytes_string(G[0][0])) + \
        bytes_string2bit(field2bytes_string(G[0][1])) + bytes_string2bit(field2bytes_string(pk[0])) + \
            bytes_string2bit(field2bytes_string(pk[1]))
    za = hex(int(za, 2))[2:]
    za_len = ((len(za) + 1) >> 1) << 1
    za = hash_sha1(bytes.fromhex(za.zfill(za_len)))
    file_in.write("签名方标识符\n{0}".format(za))
    print("签名方表示符：{0}".format(za))
    file_in.close()

    k = randint(1, G_n[0] >> 1)
    tmp = signature(message, za, k, da)
    while(tmp == None):
        k = randint(1, G_n[0] >> 1)
        tmp = signature(message, za, da, k)
    
    file_in = open("message.txt", "a+", encoding = 'utf-8')
    file_in.write('\n签名\n' + str(tmp[0]) + ' ' + str(tmp[1]))
    print("签名的消息为{0}\n--------------签名方签名完成----------------\n".format(tmp))
    file_in.close()

    sem.release()
    



# 一些没有必要的过程进行简化, 部分过程标准文档过于麻烦则简化了
# za为关于用户 A 的可辨别标识、部分椭圆曲线系统参数和用户 A 公钥的杂凑值
# k为用户A随机选择的点
# pa为用户A的公钥

def delete_message():
    file_in = open("message.txt", "r", encoding = 'utf-8')
    res = []
    tmp = file_in.readline()
    while(tmp != '签名\n'):
        res.append(tmp)
        tmp = file_in.readline()
    file_in.close()
    file_in = open("message.txt", "w", encoding = 'utf-8')
    for i in res:
        file_in.write(i)
    file_in.close()
    

def authen(message, signa, za, pa):

    r = bytes_string2int(signa[0])
    if(r >= G_n[0] or r < 1):
        print('Authencation Failure')

    s = bytes_string2int(signa[1])
    if(s >= G_n[0] or s < 1):
        print('Authencation Failure')

    m = za + message
    e = bytes_string2int(hash_sha3(bytes.fromhex(m), v[1]))
    t = (r + s) % G_n[0]

    if(t == 0):
        print('Authencation Failure')
    
    point = ecc_add(ecc_mul(G[0], s), ecc_mul(pa, t))
    
    x1 = bytes_string2int(field2bytes_string(point[0]))
    
    R = (e + x1) % G_n[0]

    if(R == r):
        return True
    
    print('Authencation Failure')


def author(sem):
    sem.acquire()
    print("-----------------验证方开始验证----------------------------\n")
    file_in = open("message.txt", "r", encoding = 'utf-8')

    message = ''
    tmp = file_in.readline()
    while(tmp != '消息\n'):
        tmp = file_in.readline()
    tmp = file_in.readline()
    while(tmp != '\n'):
        message = message + tmp
        tmp = file_in.readline()

    print("从message.txt中读取到的消息为:{0}\n".format(message))
    message = bytes(message, encoding = 'utf-8').hex()
    print("消息摘要的16进制表示为:{0}".format(message))

    tmp = file_in.readline()
    while(tmp != '签名\n'):
        tmp = file_in.readline()
    r, s = (file_in.readline()).split(" ")
    print("从message.txt中读取到的公钥为{0}".format('(' + str(r) + ', ' + str(s) + ')'))
    file_in.close()
    delete_message()

    if(int(r, 16) >= G_n[0] and int(r, 16) < 1):
        print("r value Error!")
        exit()
    if(int(s, 16) >= G_n[0] and int(s, 16) < 1):
        print("s value Error!")
        exit()

    signa = (r, s)

    file_in = open("signature.key", "r", encoding = 'utf-8')
    
    tmp = file_in.readline()
    while(tmp != '公钥部分\n'):
        tmp = file_in.readline()
    tmp = file_in.readline()
    x, y = tmp.split(" ")
    
    pk = (int(x), int(y[:-1]))

    print("从signature.key中读取到的签名方公钥为{0}\n".format('(' + x + ' ' + y[:-1] + ')'))

    tmp = file_in.readline()
    while(tmp != '签名方标识符\n'):
        tmp = file_in.readline()
    za = file_in.readline()
    
    print("从signature.key中读取到的签名方标识符为{0}".format(za))
    file_in.close()

    print('判断的结果为:' + str(authen(message, signa, za, pk)))
    print("\n随机换用另外一个签名方表示符来判断", end = ' ')

    za = hex(randint(1, G_n[0]))[2:]
    za = hash_sha1(bytes(za, encoding = 'utf-8'))
    print('新的表示符为：{0}'.format(za))
    print("判断的结果是:",end = '')
    authen(message, signa, za, pk)
    print('---------------------------验证结束----------------------------')



if(__name__ == '__main__'):

    sem = threading.Semaphore(value = 0)
    thread_signature = threading.Thread(target = signatureor, args = (sem,))
    thread_auth = threading.Thread(target = author, args = (sem,))
    thread_signature.start()
    thread_auth.start()