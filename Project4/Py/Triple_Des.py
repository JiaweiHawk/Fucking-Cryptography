'''*****************************************************************************************
   ** FileName:        Triple_Des.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-27 星期三 14:15:20
   ** Description:     编写三重DES加解密 
   **************************************************************************************'''

from Des_16 import encode, decode

def encode_triple(in_64, key1, key2):
    return encode(decode(encode(in_64, key1), key2), key1)

def decode_triple(in_64, key1, key2):
    return decode(encode(decode(in_64, key1), key2), key1)

#if( __name__ == '__main__'):

'''*****************************************************************************************
   ** Date:            2019-03-27 星期三 14:23:20
   ** Description:     单独加密64位bit信息
   **************************************************************************************'''

message = input('请输入16进制明文:')[2:]                                           
message = (bin(int(message, 16))[2:]).zfill(64)                                  
key1 = input('请输入第一位16进制密钥:')[2:]                               
key1_encode = (bin(int(key1, 16))[2:]).zfill(64)
key2 = input('请输入第二位16进制密钥:')[2:]                               
key2_encode = (bin(int(key2, 16))[2:]).zfill(64)

print('密钥为：{0}'.format('第一个秘钥为：' '0x' + key1_encode + '  ' + '第二个秘钥为：' '0x' + key2_encode) )             
cipher = encode_triple(message, key1_encode, key2_encode)                    
print('最终密文输出为：{0}'.format('0x' + cipher) ) 

print("")

cipher = input('请输入16进制密文:')[2:]                                  
key1 = input('请输入第一位16进制密钥:')[2:]                               
key1_decode = (bin(int(key1, 16))[2:]).zfill(64)
key2 = input('请输入第二位16进制密钥:')[2:]                               
key2_decode = (bin(int(key2, 16))[2:]).zfill(64)

print('密钥为：{0}'.format('第一个秘钥为：' '0x' + key1_encode + '  ' + '第二个秘钥为：' '0x' + key2_encode) )             
message = decode_triple(cipher, key1_decode, key2_decode)              
print('最终明文输出为：{0}'.format( '0x' + (hex(int(message, 2))[2:]).zfill(16))) 
input()




"""****************************************************************************************
 ** Date:            2019-03-23 星期六 19:54:12
 ** Description:     输入数据
                     message: 0x02468aceeca86420
                     key1:    0x0f1571c947d9e859    key2:  0x1e1571c947d9e859
                     cipher:  0x4f950d99df609f29
 ****************************************************************************************"""
