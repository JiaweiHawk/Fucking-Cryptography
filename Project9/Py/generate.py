"""****************************************************************************************
 ** FileName:       generate.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-28 星期二 00:16:24
 ** Description:    实现对于英文消息找出其m/2个消息变形
 ****************************************************************************************"""

"""****************************************************************************************
 ** Date:           2019-05-28 星期二 00:22:42
 ** Description:    我们通过给消息添加随机的m/2处位置选择添加 \t\b 即可， 明文看起来并没有改变
                    但实际上消息已经改变
 ****************************************************************************************"""
from copy import deepcopy
# pad = [' \b']


# def generate(message, number):
#     number = int(2 ** ( (number + 1) >> 1))

#     res = [message]
#     tmp = message

#     while(len(res) < number):
#         tmp = tmp + pad[0]
#         res.append(tmp)
#         print(tmp)
#     return res


# if(__name__ == '__main__'):
#     res = generate('I w', 8)
#     for i in range(len(res)):
#         print(res[i])


def generate(message, number):
    index = {}
    
    message = message.replace(',', '')
    message = message.replace('.', '')
    message = message.replace('!', '')
    message = message.replace('?', '')
    message = message.split(' ')
    length_message = len(message)
    length_dic = len(dic)
    for i in range(length_message):
        for z in range(length_dic):
            if(message[i] in dic[z]):
                index[i] = z
    
    res = [' '.join(message)]
    num = 1
    count = 0
    for i in index.keys():
        for k in range(num):
            tmp1 = deepcopy(res[k]).split(" ")
            for j in dic[index[i]]:
                if(j != tmp1[i]):
                    tmp = deepcopy(tmp1)
                    tmp[i] = j
                    res.append(' '.join(tmp))
                    count = count + 1
        num = num + count
        count = 0
        if(num > number):
            return res
    return res

dic = [
    ['cure', 'treay'],
    ['apparent', 'obvious', 'evident', 'clear'],
    ['eventually', 'finally'],
    ['sufficiently', 'adequately', 'enough'],
    ['little', 'tiny', 'small'],
    ['present', 'gift'],
    ['allow', 'permit'],
    ['quick', 'fast', 'rapid', 'prompt'],
    ['positive', 'sure', 'certain'],
    ['abandon', 'desert', 'forsake', 'leave'],
    ['ability', 'capacity', 'capability', 'genius', 'talent'],
    ['abolish', 'cancel', 'repeal'],
    ['accident', 'incident', 'event', 'occurrence'],
    ['only', 'just']
]



if(__name__ == '__main__'):
    file_in = open("message.txt", "r")
    message = ''
    tmp = file_in.readline()
    while(tmp != ''):
        message = message + tmp
        tmp = file_in.readline()
    file_in.close()

    number = 10                 # 即2 ^ (2/number)
    message = generate(message, 2 ** (number >> 1))
    for i in range(2 ** (number >> 1)):
        print('第{0}条信息:'.format(str(i + 1)))
        print(message[i])