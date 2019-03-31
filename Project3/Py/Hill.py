'''*****************************************************************************************
   ** FileName:        Hill.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-13 星期日 15:11:20
   ** Description:     编写程序实现对m维Hill密码的已知明文攻击
   **************************************************************************************'''


"""****************************************************************************************
 ** Date:            2019-03-17 星期天 14:43:31
 ** Description:     预备算法：欧几里得算法及欧几里得扩展算法
 ****************************************************************************************"""


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
   ** Date:            2019-03-13 星期日 15:14:20
   ** Description:     实现m维矩阵的乘、求逆、求行列式
   **************************************************************************************'''
def init(m):                    #矩阵的初始化
    matrix = []
    print("共输入{0} * {0} 个数".format(m))
    for i in range(m):
        matrix.append([])
        for j in range(m):
            matrix[i].append( int(input("请输入({0}，{1})的值：".format(i + 1, j + 1))) % 26 )
    return matrix

            
def inv(matrix):                #求矩阵的逆，返回Amod(256)的A    默认矩阵在mod256下可逆
    if(matrix == None):
        return None
    A = []
    length = len(matrix)
    for i in range(length):
        tmp = [0] * length
        tmp[i] = 1
        A.append(tmp)
    for row in range(length):
        a = matrix[row][row]
        if( a == 0):
            for j in range(row + 1, length):
                if(matrix[j][row] != 0):
                    for i in range(length):
                        matrix[row][i] = matrix[row][i] + matrix[j][i]
                        A[row][i] = A[row][i] + A[j][i]
                        a = matrix[row][row]
                    break
                else:
                    return None
        for j in range(length):
            if( j != row and matrix[j][row] != 0):
                d = gcd(a, matrix[j][row])
                tmp = int(a / d)
                tmp1 = int(matrix[j][row] / d)
                for i in range(length):
                    A[j][i] = A[j][i] * tmp - A[row][i] * tmp1
                    matrix[j][i] = matrix[j][i] * tmp - matrix[row][i] * tmp1
    for row in range(length):
        if( gcd(matrix[row][row], 26) != 1):
            return None
        a = euc_ext(matrix[row][row], 26)[0]
        for i in range(length):
            A[row][i] = (A[row][i] * a) % 26  
    return A


def show(matrix):
    m = len(matrix)
    for i in range(m):
        for j in range(m):
            #print('{0} {1}'.format(i, j))
            print(matrix[i][j], end = '  ')
        print('')

def mul(a, b):                  #矩阵的相乘
    if(a == None or b == None):
        return None
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
                sum = (sum + a[i][k] * b[k][j]) % 26
            res[i].append(sum)
    return res
    





'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 15:14:20
   ** Description:     实现m维Hill密码的加密和解密
   **************************************************************************************'''

def mess2stream(message, m):               #将消息分块成流0 - 15 即4bit一分，对于不能凑为整数的，用0补全（’asd中‘）->[97, 115, 100, 0, 156, 45, 0]
    ans = []
    for i in message:
        j = bin(ord(i))[2:]
        ans.append(16)
        j = j.zfill( int((len(j) + 3) / 4) * 4)
        while(len(j) > 3):
            ans.append(int(j[:4], 2) )
            j = j[4:]
        ans.append(16)
    length = len(ans)
    m = m * m
    if( length % m != 0):
        ans = ans + [17] * (m - (length % m) )
    return ans    

def stream2mess(stream):                #将编码流转换为消息
    flag = 0
    tmp = []
    res = []
    for i in stream:
        if(flag == 1):
            if(i == 16):
                res.append(chr(int(''.join(tmp), 2) ))
                tmp = []
                flag = 0
            else:
                tmp.append(bin(i)[2:].zfill(4))
        else:
            if(i == 17):
                break
            if(i == 16):
                flag = 1
    return res


def hill_key(m):                      #生成Hill密码矩阵
    return init(m)

def hill_encode(keys, message):           #进行加密, 输入为信息流，输出为流密文矩阵、流密文
    tmp = []
    cipher = []
    length = len(message)
    m = len(keys)
    index = 0
    while(index != length):
        for i in range(m):
            tmp.append([])
            for j in range(m):
                tmp[i].append(message[index + i * m + j])
        tmp = mul(tmp, keys)
        for i in tmp:
            for j in i:
                cipher.append(chr(j + 97) )
        index = index + m * m
        tmp = []
    return cipher


def hill_decode(keys, cipher):            #进行解密，输出为明文信息流
    message = []
    tmp = []
    k = inv(keys)
    if(k == None):
        print('矩阵不可逆')
        return None
    cipher_matrix = []
    length = len(keys)
    length2 = length * length
    index = -1
    count = -1
    for i in range(len(cipher)):
        if(i % length2 == 0):
            cipher_matrix.append([])
            index = index + 1
            count = -1


        if(i % length == 0):
            cipher_matrix[index].append([])
            count = count + 1
        cipher_matrix[index][count].append(ord(cipher[i]) - 97)  

    for i in cipher_matrix:
        tmp = mul(i, k)
        for j in tmp:
            for c in j:
                message.append(c)
    return message

# m = int(input("请输入Hill矩阵维数："))
# message = input("请输入明文信息：")
# message_stream = mess2stream(message, m)

# keys = hill_key(m)

# cipher = hill_encode(keys, message_stream)

# print('加密的信息为:{0}'.format(''.join(cipher)) )
# print('原信息为：{0}\n解密的信息为:{1}'.format(message, ''.join(stream2mess(hill_decode(keys, cipher)))) )







"""****************************************************************************************
 ** FileName:        Hill.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-03-17 星期天 21:43:37
 ** Description:     更高效的实现，直接经行utf-8的变换
 ****************************************************************************************"""



'''*****************************************************************************************
   ** Date:            2019-03-13 星期日 15:14:20
   ** Description:     实现m维矩阵的乘、求逆、求行列式
   **************************************************************************************'''

         
# def inv_8(matrix):                #求矩阵的逆，返回Amod(256)的A    默认矩阵在mod256下可逆
#     A = []
#     length = len(matrix)
#     for i in range(length):
#         tmp = [0] * length
#         tmp[i] = 1
#         A.append(tmp)
#     for row in range(length):
#         a = matrix[row][row]
#         for j in range(length):
#             if( j != row and matrix[j][row] != 0):
#                 d = gcd(a, matrix[j][row])
#                 tmp = int(a / d)
#                 tmp1 = int(matrix[j][row] / d)
#                 for i in range(length):
#                     A[j][i] = A[j][i] * tmp - A[row][i] * tmp1
#                     matrix[j][i] = matrix[j][i] * tmp - matrix[row][i] * tmp1
#     for row in range(length):
#         a = euc_ext(matrix[row][row], 256)[0]
#         for i in range(length):
#             A[row][i] = (A[row][i] * a) % 256  
#     return A


# def show_8(matrix):
#     m = len(matrix)
#     for i in range(m):
#         for j in range(m):
#             #print('{0} {1}'.format(i, j))
#             print(matrix[i][j], end = '  ')
#         print('')

# def mul_8(a, b):                  #矩阵的相乘
#     alen = len(a)
#     blen = len(b)
#     if( alen != blen):
#         return None
#     res = []
#     for i in range(alen):
#         res.append([])
#         for j in range(alen):
#             sum = 0
#             for k in range(alen):
#                 sum = sum + a[i][k] * b[k][j]
#             res[i].append(sum % 256)
#     return res
    





# '''*****************************************************************************************
#    ** Date:            2019-03-13 星期日 15:14:20
#    ** Description:     实现m维Hill密码的加密和解密
#    **************************************************************************************'''

# def mess2stream_8(message, m):               #将消息分块成流0 - 255 即一个字节一分，对于不能凑为整数的，用0补全（’asd中‘）->[97, 115, 100, 0, 156, 45, 0]
#     ans = []
#     for i in message:
#         j = bin(ord(i))[2:]
#         if( len(j) > 8):
#             ans.append(0)
#             j = j.zfill( int((len(j) + 7) / 8) * 8)
#             while(len(j) > 7):
#                 ans.append(int(j[:8], 2) )
#                 j = j[8:]
#             ans.append(0)
#         else:
#             ans.append(int(j, 2) )
#     length = len(ans)
#     m = m * m
#     if( length % m != 0):
#         ans = ans + [1] * (m - (length % m) )
#     return ans    

# def stream2mess_8(stream):                #将编码流转换为消息
#     flag = 0
#     tmp = []
#     res = []
#     for i in stream:
#         if(flag == 1):
#             if(i == 0):
#                 res.append(chr(int(''.join(tmp), 2) ))
#                 tmp = []
#                 flag = 0
#             else:
#                 tmp.append(bin(i)[2:].zfill(8))
#         else:
#             if(i == 1):
#                 break
#             if(i == 0):
#                 flag = 1
#             else:
#                 res.append(chr(i))
#     return res


# def hill_encode_8(keys, message):           #进行加密, 输入为信息流，输出为流密文矩阵、流密文
#     cipher_matrix = []
#     tmp = []
#     cipher = []
#     length = len(message)
#     m = len(keys)
#     index = 0
#     while(index != length):
#         for i in range(m):
#             tmp.append([])
#             for j in range(m):
#                 tmp[i].append(message[index + i * m + j])
#         tmp = mul_8(tmp, keys)
#         for i in tmp:
#             for j in i:
#                 cipher.append(j)
#         cipher_matrix.append(tmp)
#         index = index + m * m
#         tmp = []
#     return cipher_matrix, cipher


# def hill_decode_8(keys, cipher):            #进行解密，输出为流明文
#     message = []
#     tmp = []
#     k = inv_8(keys)
#     for i in cipher:
#         tmp = mul_8(i, k)
#         for j in tmp:
#             for c in j:
#                 message.append(c)
#     return message




"""****************************************************************************************
 ** Date:            2019-03-18 星期一 20:50:16
 ** Description:     实现对m维Hill的已知明文攻击
 ****************************************************************************************"""

def attack(message, cipher, m):
    message_stream = mess2stream(message, m)
    cipher_stream = []
    for i in cipher:
        cipher_stream.append(ord(i) - 97)
    index = - m * m
    flag = None
    used_message = []
    used_cipher = []
    message_matrix = []
    while(flag == None):
        index = index + m * m
        message_matrix = []
        for i in range(m):
                message_matrix.append([])
                for j in range(m):
                    if(index + i * m + j >= len(message_stream)):
                        print("输入太短")
                        return None
                    message_matrix[i].append(message_stream[index + i * m + j])
        flag = inv(message_matrix)

    for i in range(index, index + m * m):
        used_message.append(str(message_stream[i]) )

    cipher_matrix = []
    for i in range(m):
                cipher_matrix.append([])
                for j in range(m):
                    cipher_matrix[i].append(cipher_stream[index + i * m + j])
                    used_cipher.append(str(cipher_stream[index + i * m + j]))
    return mul(flag, cipher_matrix), '_'.join(used_message), '_'.join(used_cipher)


m = int(input("请输入Hill矩阵维数："))
message = input("请输入明文信息：")
message_stream = mess2stream(message, m)

keys = hill_key(m)
k = []
for i in range(m):
    k.append([])
    for j in keys[i]:
        k[i].append(j)
cipher = hill_encode(keys, message_stream)

print('加密的信息为:{0}'.format(''.join(cipher)) )
print('原信息为：{0}\n解密的信息为:{1}'.format(message, ''.join(stream2mess(hill_decode(keys, cipher)))) )
print('原Hill加密矩阵：')
show(k)

key, used_message, used_cipher = attack(message, cipher, m)
print('使用明文对：{0}\n使用密文对：{1}'.format(used_message, used_cipher))
print('通过明密文对求解出的Hill加密矩阵位：')
show(key)

input()