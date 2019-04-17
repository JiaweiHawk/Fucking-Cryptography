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


def ctr_one(message, key, t):
    t =  aes(t, key)
    length = len(message)
    res = [0] * length
    for i in range(length):
        res[i] = hex(int(message[i], 16) ^ int(t[i], 16))[2:]
    return ''.join(res)

'''*****************************************************************************************
   ** Date:            2019-04-10 星期三 15:14:10
   ** Description:     实现文件的二进制读写
   **************************************************************************************'''
def ctr(in_path, out_path, key, t):
    if (not os.path.exists(in_path)):
        print("File doesn't exits")
        return None
    file_in = open(in_path, "rb")
    file_out = open(out_path, 'wb')
    string = file_in.read(16).hex()
    key = (hex(int(key, 16))[2:]).zfill(32)
    while(string != ''):
        file_out.write(bytes.fromhex(ctr_one(string, key, (hex(t)[2:]).zfill(32))))
        string = file_in.read(16).hex()
        t = t + 1
    file_in.close()
    file_out.close()
if(__name__ == '__main__'):
    in_path = 'D:/data/北航/2019春季/密码学与网络安全/试验/实验5/Py/message.png'
    out_path = 'D:/data/北航/2019春季/密码学与网络安全/试验/实验5/Py/cipher.txt'
    tmp = 'D:/data/北航/2019春季/密码学与网络安全/试验/实验5/Py/plaintext.png'
    ctr(in_path, out_path, '0f1571c947d9e8590cb7add6af7f6798', 158423)
    ctr(out_path, tmp, '0f1571c947d9e8590cb7add6af7f6798', 158423)
