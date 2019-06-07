"""****************************************************************************************
 ** FileName:       sha3.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-18 星期六 23:10:14
 ** Description:    实现SHA-3
                    所有接口为2进制
 ****************************************************************************************"""
from hashlib import sha3_224, sha3_256, sha3_384, sha3_512
from sha3_math import theta, rho, pi, chi, iota, state2array, array2state, Para, xor, code_string


"""****************************************************************************************
 ** Date:           2019-05-22 星期三 11:52:07
 ** Description:    注意SHA-3的填充规则
                    1，把填充的比特串按每字节  高位在后，低位在前 转换（即每字节二进制字符串逆置）
                    2、小端转换是 8 字节，类似于 C语言 long 类型转换
                    3、假如填充完一组明文后（明文总共一组 r-8 bit 明文，那么填充后明文后，需加 16 进制 86   此处是重点*******）
 ****************************************************************************************"""



def pre_deal(message, mode):
    message = code_string(message)                  #首先将其转换成小段
    length = len(message)
    pad_length = (-length - 4) % Para[mode][0]
    message = message + '011' + '0' * pad_length + '1'
    length = (length + pad_length + 4) // Para[mode][0]
    ans = [None] * length
    for i in range(length):
        ans[i] = message[i * Para[mode][0]: (i + 1) * Para[mode][0]] + '0' * Para[mode][1]# code_string(message[i * Para[mode][0]: (i + 1) * Para[mode][0]] + '0' * Para[mode][1])

    return ans


def f(array):           # 输入的为array类型                 
    for i in range(24):
        array = iota(chi(pi(rho(theta(array)))), i)
    return array


def hash_sha3(message, mode):          #实现sha, 输入为bytes类型


    length = len(message) << 3                  # 将bytes转换为二进制字符串
    if( message == b''):
        message = ''
    else:
        message = (bin(int(message.hex(), 16))[2:]).zfill(length)

    message = pre_deal(message, mode)
    length = len(message)

    array = state2array('0' * 1600)
    for i in range(length):
        array = f(xor(array, state2array(message[i])))
    hash_value = code_string(array2state(array)[:mode]) # 转换成小段，即每个字节颠倒顺序
    
    return (hex(int(hash_value, 2))[2:]).zfill(mode >> 2)


if(__name__ == '__main__'):

    file_in = open("message.txt", "r")
    message = ''
    tmp = file_in.readline()
    while(tmp != ''):
        message = message + tmp
        tmp = file_in.readline()
    
    file_in.close()


    print("从message.txt文件中读入的消息为:{0}\n".format(message))

    message = message.encode(encoding = 'utf-8')


    # sha3-224
    mode = 224
    print('使用自己编写的SHA3_224得到的结果为:{0}'.format(hash_sha3(message, mode)))
    Hash = sha3_224()
    Hash.update(message)
    print('                系统调用的SHA3-224:' + Hash.hexdigest())
    print('')

    # sha3-256
    mode = 256
    print('使用自己编写的SHA3_256得到的结果为:{0}'.format(hash_sha3(message, mode)))
    Hash = sha3_256()
    Hash.update(message)
    print('                系统调用的SHA3-256:' + Hash.hexdigest())
    print('')


    # sha3-384
    mode = 384
    print('使用自己编写的SHA3_384得到的结果为:{0}'.format(hash_sha3(message, mode)))
    Hash = sha3_384()
    Hash.update(message)
    print('                系统调用的SHA3-384:' + Hash.hexdigest())
    print('')



    # sha3-512
    mode = 512
    print('使用自己编写的SHA3_512得到的结果为:{0}'.format(hash_sha3(message, mode)))
    Hash = sha3_512()
    Hash.update(message)
    print('                系统调用的SHA3-512:' + Hash.hexdigest())
    print('')

    