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

def u2b(message):                   #将输入信息转换为二进制字符串('ab' -> ['0010', '0010'])
    data = []
    for i in message:
        data.append(bin(ord(i))[2:].zfill(7))
    return ''.join(data)


def b2u(blist):                     #将二进制字符串列表转换为UTF-8编码的字符串(['0010','0010]) ->'ab'
    a = []
    while(len(blist) > 6):
        a.append( chr(int(blist[:7], 2) ) )
        blist = blist[7:]
    return ''.join(a)


def ver_key():                      #生成弗纳姆密码表   48为ord('0')
    return input("请输入弗纳姆密码表(二进制字符串)：")


def ver_encode(keys, message):           #进行加密, 输入为二进制字符串明文及二进制字符串密钥，输出为二进制字符串密文
    cipher = []
    length = len(keys)
    index = 0
    for i in message:
        if(index == length):
            index = 0
        cipher.append(chr(48 + (ord(i) ^ ord(keys[index]))))
        index = index + 1
    return ''.join(cipher)


def ver_decode(keys, cipher):            #进行解密，输入为二进制字符串明文及二进制字符串密钥，输出为二进制字符串明文
    message = []
    length = len(keys)
    index = 0
    for i in cipher:
        if(index == length):
            index = 0
        message.append(chr(48 + (ord(i) ^ ord(keys[index]))))
        index = index + 1
    return b2u(''.join(message) )


message = input("请输入明文信息：")
b_message = u2b(message)
print('明文信息的二进制表达：{0}'.format(''.join(b_message)) )

keys = ver_key()

cipher = ver_encode(keys, b_message)
print('加密的信息为：{0}'.format(cipher) )
print('原信息为：{0}\n解密的信息为:{1}'.format(message, ver_decode(keys, cipher)) )
input()