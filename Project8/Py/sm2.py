"""****************************************************************************************
 ** FileName:       sm2.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-16 星期四 17:39:26
 ** Description:    实现SM2的加、解密算法
                    接口是16进制
 ****************************************************************************************"""

from hashlib import sha1, md5
from ecc import ecc_mul, G, p, p_len, G_n, Infin, a, b
from random import randint
from sm2_math import bit2bytes_string, bytes_string2bit, point2bytes_string, field2bytes_string, bytes_string2point
import threading

file_max = [1024]       #读入文件的最大值
v = [160, 128]         #v[0]指密钥杂凑算法的输出bit数，v[1]表示加密时的Hash函数输出bit数


"""****************************************************************************************
 ** Date:           2019-05-18 星期六 14:55:34
 ** Description:    加密方的组件
                    包括KDF算法（其中hash函数选择Sha1（），可以随意修改成其他的)
                    读取公钥。
 ****************************************************************************************"""

def get_key():
    key_file = open("sm2.key", "r", encoding = 'utf-8')

    k = key_file.readline()
    while(k != '公钥部分\n'):
        k = key_file.readline()
    k = key_file.readline()
    key_file.close()

    k = k.split(" ")                #p,n默认易知， 仅需要读取椭圆曲线的点即可
    return (int(k[0]), int(k[1]))

# 实现密钥派生函数
def kdf(z, klen):   #klen为bit长度
    z = bytes.fromhex(bit2bytes_string(z))

    num = (klen + v[0] - 1) // v[0]
    H = [None] * (num)
    ct =0x00000001
    for i in range(num - 1):
        Hash = sha1()
        hash_in = z + bytes.fromhex((hex(ct)[2:]).zfill(8))
        Hash.update(hash_in)
        H[i] = (bin(int(Hash.hexdigest(), 16))[2:]).zfill(v[0])
        ct = ct + 1
    
    Hash = sha1()
    hash_in = z + bytes.fromhex((hex(ct)[2:]).zfill(8))
    Hash.update(hash_in)
    ha = (bin(int(Hash.hexdigest(), 16))[2:]).zfill(v[0])

    if(num * v[0] == klen):
        H[num - 1] = ha
    else:
        H[num - 1] = ha[:klen - v[0] * (klen // v[0])]
    
    return ''.join(H)


def encode(pk, message):
    klen = (len(message)) << 2
    random_k = randint(1, G_n[0] - 1)

    s = ecc_mul(pk, random_k)
    if(s == Infin[0]):
        print("s == O!Error")
        exit()

    t_in = bytes_string2bit(field2bytes_string(s[0])) + bytes_string2bit(field2bytes_string(s[1]))
    t = kdf(t_in, klen)
    while(t == '0' * klen):
        random_k = randint(1, G_n[0] - 1)
        s = ecc_mul(get_key(), random_k)
        if(s == Infin[0]):
            print("s == O!Error")
            exit()
        t_in = bytes_string2bit(field2bytes_string(s[0])) + bytes_string2bit(field2bytes_string(s[1]))
        t = kdf(t_in, klen)
    
    c1 = point2bytes_string(ecc_mul(G[0], random_k))

    Hash = md5()
    Hash.update(bytes.fromhex(field2bytes_string(s[0]) + message + field2bytes_string(s[1])))

    c3 = Hash.hexdigest()

    c2 = (hex(int(message, 16) ^ int(t, 2))[2:]).zfill(klen >> 2)

    return  c1 + c3 + c2


def encoder(sem_encode, sem_decode): 
    sem_encode.acquire()
    print('\n加密开始')
    print('加密方成功读取sm2.key文件')
    pk = get_key()


    file_in = open("message.txt", "rb")
    message = file_in.read(file_max[0]).hex()
    file_in.close()

    print('要加密的明文文件为message.txt,内容为:\n', end = '')
    print(bytes.fromhex(message).decode(encoding = 'utf-8'))

    cipher = encode(pk, message)

    print('\n加密的密文是\n{0}, 放在cipher.sm2文件中'.format(str(cipher)))

    file_out = open("cipher.sm2", 'wb')
    file_out.write(bytes.fromhex(cipher))
    file_out.close()
    sem_decode.release()


# """****************************************************************************************
#  ** Date:           2019-05-18 星期六 14:54:57
#  ** Description:    解密方的组件
#                     包括生成公钥
#                     解密
#  ****************************************************************************************"""




# 生成解密方的公钥，
def key_generate(k):
    key_file = open("sm2.key", "w", encoding = 'utf-8')
    key_file.write('公钥部分\n')
    point = ecc_mul(G[0], k)
    key_file.write(str(point[0]) + ' ' + str(point[1]) + ' \n')
    key_file.close()


def decode(cipher, random_k):
    c1_len = ((((p_len[0] + 7) >> 3) << 1) + 1) << 1

    z = bytes_string2point(cipher[:c1_len])
    if( (z[1] * z[1]) % p[0] != (z[0] ** 3 + a[0] * z[0] + b[0]) % p[0]):
        print("Error! Not in ecc")
        exit()
        
    s = ecc_mul(z, random_k)
    if(s == Infin[0]):
        print('S = O!Error!')
        exit()

    cipher = cipher[c1_len:]

    c3 = cipher[:v[1] >> 2]
    cipher = cipher[v[1] >> 2:]

    klen = len(cipher)

    t_in = bytes_string2bit(field2bytes_string(s[0])) + bytes_string2bit(field2bytes_string(s[1]))
    t = kdf(t_in, klen << 2)

    message = (hex(int(cipher, 16) ^ int(t, 2))[2:]).zfill(klen)

    Hash = md5()
    Hash.update(bytes.fromhex(field2bytes_string(s[0]) + message + field2bytes_string(s[1])))

    if(Hash.hexdigest() != c3):
        print('Error!Decode is not match!')
        exit()

    return message
    


# 构建多线程中代表解密的线程
# 其作用是生成公钥供加密方使用
# 等加密方加密完后开始解密
def decoder(sem_encode, sem_decode): 
    random_k = randint(1, G_n[0] - 1)
    key_generate(random_k)
    print('\n解密方公钥成功生成在sm2.key文件中')

    sem_encode.release()


    sem_decode.acquire()
    print('\n开始解密：')
    file_in = open("cipher.sm2", "rb")
    cipher = file_in.read(file_max[0]).hex()
    file_in.close()

    print('读取的密文为:\n', end = '')
    print(cipher)

    message = bytes.fromhex(decode(cipher, random_k))

    print('\n解密的明文:\n', end = '')
    print(message.decode(encoding = 'utf-8'))

    file_out = open('message_sm2.txt', 'wb')
    file_out.write(message)
    print('解密方解密内容成功生成在message_sm2.txt文件中\n')



if(__name__ == '__main__'):

    sem_decode = threading.Semaphore(value = 0)
    sem_encode = threading.Semaphore(value = 0)
    thread_decoder = threading.Thread(target = decoder, args = (sem_encode, sem_decode))
    thread_encoder = threading.Thread(target = encoder, args = (sem_encode, sem_decode))
    thread_decoder.start()
    thread_encoder.start()


    