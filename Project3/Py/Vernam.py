'''*****************************************************************************************
   ** FileName:        Vernam.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-13 星期日 14:40:20
   ** Description:     编程实现弗纳姆密码
   **************************************************************************************'''




'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 17:16:20
   ** Description:     加密、解密算法
   **************************************************************************************'''

def u2b(message):                   #将输入信息转换为二进制字符串存储在列表中('ab' -> ['0010', '0010'])
    data = []
    for i in message:
        data.append(str(bin(ord(i)))[2:])
    return data


def b2u(blist):                     #将二进制字符串列表转换为UTF-8编码的字符串(['0010','0010]) ->'ab'
    return ''.join( [chr(int(i, 2)) for i in blist] )


def ver_key():                      #生成弗纳姆密码表   48为ord('0')
    a = input("请输入弗纳姆密码表(二进制字符串)：")
    return [ord(i) for i in a]


def ver_encode(keys, message):           #进行加密, 输入为二进制字符串明文及二进制字符串密钥，输出为二进制字符串密文
    cipher = []
    length = len(keys)
    index = 0
    tmp = []
    for i in message:
        for j in i:
            if(index == length):
                index = 0
            tmp.append(chr( (keys[index] ^ ord(j)) + 48) )
            index = index + 1
        cipher.append(''.join(tmp) )
        tmp = []
    return cipher


def ver_decode(keys, cipher):            #进行解密，输入为二进制字符串明文及二进制字符串密钥，输出为二进制字符串明文
    message = []
    length = len(keys)
    index = 0
    tmp = []
    for i in cipher:
        for j in i:
            if(index == length):
                index = 0
            tmp.append(chr( (keys[index] ^ ord(j)) + 48) )
            index = index + 1
        message.append(''.join(tmp) )
        tmp = []
    return message


message = input("请输入明文信息：")
b_message = u2b(message)
print('明文信息的二进制表达：{0}'.format('_'.join(b_message)) )

keys = ver_key()

b_cipher = ver_encode(keys, b_message)
cipher = b2u(b_cipher)
print('加密的信息为：{0}  二进制表达为{1}'.format(cipher, '_'.join(b_cipher)) )
print('原信息为：{0}\n解密的信息为:{1}'.format(message, b2u(ver_decode(keys, b_cipher))) )
input()