"""****************************************************************************************
 ** FileName:       Elgamal.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-15 星期三 22:37:15
 ** Description:    实现Elgamal加密算法与解密算法
                    所有接口仍然是16进制
 ****************************************************************************************"""
from ecc import ecc_mul, G, G_n, p_len, p, euc_ext
from random import randint
import threading

"""****************************************************************************************
 ** Date:           2019-05-16 星期四 00:15:13
 ** Description:    加密方的组件，包括
                    读取解密方的公钥
                    消息加密
 ****************************************************************************************"""


random_k = [None]


# 使用ELgamal加密给定长度的明文,其中x = k * pk的横坐标, write_size为16进制时的大小
def elgamal_multiply(write_size, x, message):
    return (hex((x * int(message, 16)) % p[0])[2:]).zfill(write_size)

def get_key():
    key_file = open("Elgamal.key", "r")

    k = key_file.readline()
    while(k != '公钥部分\n'):
        k = key_file.readline()
    k = key_file.readline()
    key_file.close()

    k = k.split(" ")                #p,n默认易知， 仅需要读取椭圆曲线的点即可
    return (int(k[0]), int(k[1]))

def encode():

    read_size = (p_len[0] - 8) >> 3
    write_size = ((p_len[0]) >> 3) << 1 #16进制长度
    pk = get_key()

    random_k = randint(1, G_n[0])
    key = ecc_mul(pk, random_k)
    while(key[0] == 0):
        random_k = randint(1, G_n[0])
        key = ecc_mul(pk, random_k)
    
    send_point = ecc_mul(G[0], random_k)

    print("加密方参数选择完毕,选取的k为{0}\n".format(str(random_k)))
    
    print('要加密的明文文件为message.txt\n', end = '')

    file_in = open("message.txt", "rb")
    file_out = open("message.elgamal", "wb")

    # 首先发送生成元的random_k乘的坐标
    file_out.write(bytes.fromhex((hex(send_point[0])[2:]).zfill(write_size)))
    file_out.write(bytes.fromhex((hex(send_point[1])[2:]).zfill(write_size)))


    message = file_in.read(read_size)
    while(message != b''):
        file_out.write(bytes.fromhex(elgamal_multiply(write_size, key[0], '11' + message.hex())))
        message = file_in.read(read_size)
    print("加密方加密结束\n")
    file_in.close()
    file_out.close()



def encoder(sem_encode, sem_decode): 
    sem_encode.acquire()
    print('\n加密开始')
    print('加密方成功读取sm2.key文件')
    pk = get_key()


    encode()
    sem_decode.release()

"""****************************************************************************************
 ** Date:           2019-05-16 星期四 00:15:34
 ** Description:    解密方的部件，包括：
                    公钥生成
                    单个消息解密
                    消息解密
 ****************************************************************************************"""


# 生成解密方的公钥，
def key_generate(k):
    key_file = open("Elgamal.key", "w")
    key_file.write('公钥部分\n')
    point = ecc_mul(G[0], k)
    key_file.write(str(point[0]) + ' ' + str(point[1]) + ' \n')
    key_file.close()


def decode(k):

    read_size = p_len[0] >> 3
    write_size = ((p_len[0] - 8) >> 3) << 1

    file_in = open("message.elgamal", "rb")
    file_out = open("message_new_elgamal.txt", "wb")

    pk = [None, None]

    # 读取输入点
    pk[0] = int(file_in.read(read_size).hex(), 16)
    pk[1] = int(file_in.read(read_size).hex(), 16)
    pk = tuple(pk)
    key = ecc_mul(pk, k)

    x = euc_ext(key[0], p[0])[0]


    cipher = file_in.read(read_size)
    while(cipher != b''):
        message = elgamal_multiply(write_size, x, cipher.hex())
        while(message[:2] != '11'):
            message = message[2:]
        message = message[2:]
        file_out.write(bytes.fromhex(message))
        cipher = file_in.read(read_size)
    


    print("解密方解密完成\n")
    
    file_in.close()
    file_out.close()


def decoder(sem_encode, sem_decode): 
    random_k = randint(1, G_n[0] - 1)
    key_generate(random_k)
    print('\n解密方公钥成功生成在sm2.key文件中')

    sem_encode.release()


    sem_decode.acquire()
    print('\n开始解密：')
    
    decode(random_k)

    print('解密方解密内容成功生成在message_sm2.txt文件中\n')



if(__name__ == '__main__'):
    sem_decode = threading.Semaphore(value = 0)
    sem_encode = threading.Semaphore(value = 0)
    thread_decoder = threading.Thread(target = decoder, args = (sem_encode, sem_decode))
    thread_encoder = threading.Thread(target = encoder, args = (sem_encode, sem_decode))
    thread_decoder.start()
    thread_encoder.start()