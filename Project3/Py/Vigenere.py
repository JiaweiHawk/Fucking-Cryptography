'''*****************************************************************************************
   ** FileName:        Vigenere.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-13 星期日 14:40:20
   ** Description:     编程实现维吉尼亚密码
   **************************************************************************************'''




'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 17:16:20
   ** Description:     加密、解密算法
   **************************************************************************************'''


def vig_key():                      #生成维吉尼亚密码
    a = input("请输入维吉尼亚密码表：")
    return [ord(i.lower()) - 97 for i in a]

def vig_encode(keys, message):           #进行加密, 输入为字母           97为ord( 'a')
    cipher = []
    length = len(keys)
    index = 0
    for i in message:
        if( i.isalpha() ):
            if(index == length):
                index = 0
            cipher.append(chr( (ord(i.lower()) - 97 + keys[index]) % 26 +97) )
            index = index + 1
    return ''.join(cipher)


def vig_decode(keys, cipher):            #进行解密，输出为字母
    message = []
    length = len(keys)
    index = 0
    for i in cipher:
        if(index == length):
            index = 0
        message.append(chr( (ord(i.lower()) - 97 - keys[index]) % 26 +97) )
        index = index + 1
    return ''.join(message)


message = input("请输入明文信息：")
keys = vig_key()
cipher = vig_encode(keys, message)
print('加密的信息为:{0}'.format(cipher) )
print('原信息为：{0}\n解密的信息为:{1}'.format(message, vig_decode(keys, cipher)) )
input()
    
