'''*****************************************************************************************
   ** FileName:        Hill.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-13 星期日 15:11:20
   ** Description:     编写程序实现对m维Hill密码的已知明文攻击
   **************************************************************************************'''


'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 15:14:20
   ** Description:     实现m维矩阵的乘、求逆、求行列式
   **************************************************************************************'''
def init(m):
    matrix = []
    data = 0
    for i in range(m):
        matrix.append([])
        for j in range(m):
            matrix[i].append( int(input("请输入（{0}，{1}）的值)：".format(i + 1, j + 1))) )
    return matrix

def show(matrix):
    m = len(matrix)
    for i in range(m):
        for j in range(m):
            print('{0} {1}'.format(i, j))
            print(matrix[i][j], end = '  ')
        print('')
        
def mul(a, b):
    alen = len(a)
    blen = len(b)
    if( alen != blen):
        return None
    res = []
    for i in range(alen):
        res.append([])
        for j in range(alen):
            sum = 0
            for k in range(alen):
                sum = sum + a[i][k] * b[k][j]
            res.append(sum)
    return res
    

a = init(2)
b = init(2)
show(a)
show(b)
show(mul(a,b))













'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 15:14:20
   ** Description:     实现m维Hill密码的加密和解密
   **************************************************************************************'''


'''def ver_key():                      #生成弗纳姆密码
    a = input("请输入维吉尼亚密码表：")
    return [ord(i.lower()) - 97 for i in a]

def ver_encode(keys, message):           #进行加密, 输入为字母           97为ord( 'a')
    cipher = []
    length = len(keys) - 1
    index = 0
    for i in message:
        if(index == length):
            index = 0
        cipher.append(chr( ( (ord(i.lower()) - 97) ^ keys[index]) % 26 +97) )
        index = index + 1
    return ''.join(cipher)


def ver_decode(keys, cipher):            #进行解密，输出为字母
    message = []
    length = len(keys) - 1
    index = 0
    for i in cipher:
        if(index == length):
            index = 0
        message.append(chr( ( (ord(i.lower()) - 97) ^ keys[index]) % 26 +97))
        index = index + 1
    return ''.join(message)


message = input("请输入明文信息：")
keys = ver_key()
cipher = ver_encode(keys, message)
print('加密的信息为{0}：'.format(cipher) )
print('原信息为：{0}\n解密的信息为:{1}'.format(message, ver_decode(keys, cipher)) )'''
    
