'''*****************************************************************************************
   ** FileName:        ctr_mode.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-04-10 星期三 15:11:10
   ** Description:     通过CTR(计数器模式)实现大批量报文加密
   **************************************************************************************'''

from Aes import aes_encode as aes
import os



'''*****************************************************************************************
   ** Date:            2019-04-10 星期三 15:14:10
   ** Description:     实现单独一个输入的加密, 仍然全部接口为不待前缀的16进制
   **************************************************************************************'''


def ctr_one(message, key, t, length):
    t =  aes(t, key)
    res = [0] * length
    for i in range(length):
        res[i] = hex(int(message[i], 16) ^ int(t[i], 16))[2:]
    return ''.join(res)

def ctr_encode(message, key, t):
   message = bytes(message, encoding = 'utf-8').hex()
   length = len(message)
   cipher = ''
   while(length >= 32):
      cipher = cipher + ctr_one(message[:32], key, (hex(t)[2:]).zfill(32), 32)
      t = (t + 1) & 0xffffffff
      length = length - 32
      message = message[32:]
   if(length > 0):
      cipher = cipher + ctr_one(message, key, (hex(t)[2:]).zfill(32), length)
      t = (t + 1) & 0xffffffff
   return t, cipher

def ctr_decode(message, key, t):
   length = len(message)
   cipher = ''
   while(length >= 32):
      cipher = cipher + ctr_one(message[:32], key, (hex(t)[2:]).zfill(32), 32)
      t = (t + 1) & 0xffffffff
      length = length - 32
      message = message[32:]
   if(length > 0):
      cipher = cipher + ctr_one(message, key, (hex(t)[2:]).zfill(32), length)
      t = (t + 1) & 0xffffffff
   cipher = (bytes.fromhex(cipher)).decode(encoding = 'utf-8')
   return t, cipher

    
if(__name__ == '__main__'):
   key = '0f1571c947d9e8590cb7add6af7f6798'
   t = 158423
   message = "asdas"
   t1, cipher = ctr_encode(message, key, t)
