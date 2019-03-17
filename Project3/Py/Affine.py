'''*****************************************************************************************
   ** FileName:        Affine.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-13 星期日 14:04:20
   ** Description:     加密解密程序实现对 P67 习题3.1
   **************************************************************************************'''



'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 14:16:20
   ** Description:     预备函数欧几里得算法、欧几里得扩展算法
   **************************************************************************************'''

def gcd(a, b):                      #Euclid算法
    if( a == 0):
        return b
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp
        tmp = a % b
    return b



def euc_ext(a, b):                      #Euclid扩展算法
    if( b == 0):
        return (0, 1)
    x_pre = 1
    x = 0
    y_pre = 0
    y = 1
    q = int( a / b)
    tmp = a % b
    while( tmp != 0):
        a = b
        b = tmp

        tmp = x_pre - q * x
        x_pre = x
        x = tmp

        tmp = y_pre - q * y
        y_pre = y
        y = tmp

        q = int(a / b)
        tmp = a % b
    return (x, y)



'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 14:16:20
   ** Description:     加密、解密算法
   **************************************************************************************'''


def aff_key():                      #生成仿射密码密码
    a = int(input("请输入第一位密钥a："))
    while( gcd(a, 26) != 1 ):
        a = int(input("密钥a应该和26互素，请重新输入第一位密钥a："))
    print("输入的秘钥a为{0}".format(a) )
    b = int(input("请输入第二位密钥b："))
    print("输入的秘钥b为{0}".format(b) )
    return (a, b)

def aff_encode(keys, message):           #进行加密, 输入为字母           97w为ord( 'a')
    cipher = []
    for i in message:
        if(i.isalpha()):
            cipher.append( chr( (keys[0] * (ord(i.lower()) - 97) + keys[1]) % 26 + 97 ) )
    return ''.join(cipher)


def aff_decode(keys, cipher):            #进行解密，输出为字母
    k = euc_ext(keys[0], 26)[0]
    message = []
    for i in cipher:
        message.append(chr(((ord(i) - 97 - keys[1]) * k ) % 26 + 97 ) )
    return ''.join(message)



message = input("请输入明文信息：")
keys = aff_key()
cipher = aff_encode(keys, message)
print('加密的信息为{0}：'.format(cipher) )
print('原信息为：{0}\n解密的信息为:{1}'.format(message, aff_decode(keys, cipher)) )
input()
    
