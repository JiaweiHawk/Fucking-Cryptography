"""****************************************************************************************
 ** FileName:        gui.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现最终的GUI界面
 ****************************************************************************************"""

from ctr_mode import ctr
from Aes import aes_encode, aes_decode
from tkinter import *
import os

"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现GUI主界面
 ****************************************************************************************"""

def window():
    root = Tk()
    root.title('Aes')
    root.geometry('550x670')
    photo = PhotoImage(file='aes.png')
    Label(root,image=photo,height=512).place(x=10,y=60)
    Label(root,text='Aes加密、解密程序',font=('黑体',20,'bold')).place(x=250,y=40,anchor=CENTER)
    Button(root,width=15,text='Aes 128bit加密',relief='sunken',bd='2',font=('黑体',10,'bold'),
           command=lambda:encode_128()).place(x=70,y=590)
    Button(root,width=15,text='Aes 128bit解密',relief='sunken',bd='2',font=('黑体',10,'bold'),
           command=lambda:decode_128()).place(x=290,y=590)
    Button(root, width=15, text='Aes ctr加密', relief='sunken', bd='2', font=('黑体', 10, 'bold'),
           command=lambda: encode_ctr()).place(x=70, y=630)
    Button(root, width=15, text='Aes ctr解密', relief='sunken', bd='2', font=('黑体', 10, 'bold'),
           command=lambda: decode_ctr()).place(x=290, y=630)
    root.mainloop()

"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现128bit GUI加密界面
 ****************************************************************************************"""


def encode_128():

    top1 = Toplevel()
    top1.geometry('800x300')

    message_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    message_get[0].place(x = 250, y=40)
    message_place = Label(top1, width=14, text='输入16进制明文:', height=1, relief='sunken', bd='2',
                      fg='blue', font=('黑体', 11, 'bold'))
    message_place.place(x=50, y=40)


    key_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    key_get[0].place(x = 250, y=100)
    key_place = Label(top1, width=14, text = '输入16进制秘钥:', height=1, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    key_place.place(x = 50, y = 100)

    bash = Label(top1, width=60, height=2, relief='sunken', bd='2',
                 fg='red', font=('黑体', 11, 'bold'))
    bash.config(text='等待设置完成')
    bash.place(x=150, y=200)

    def decode():
        bash.config(text ='加密密文为0x' + aes_encode(message_get[0].get(), key_get[0].get()))

    sub = Button(top1, width=10, text='开始加密', relief='sunken', bd='2', font=('黑体', 10, 'bold'), command=decode)
    sub.place(x=10, y=200)

    top1.mainloop()




"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现位128bit GUI解密界面
 ****************************************************************************************"""

def decode_128():

    top1 = Toplevel()
    top1.geometry('800x300')

    cipher_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    cipher_get[0].place(x = 250, y=40)
    cipher_place = Label(top1, width=14, text='输入16进制密文:', height=1, relief='sunken', bd='2',
                      fg='blue', font=('黑体', 11, 'bold'))
    cipher_place.place(x=50, y=40)


    key_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    key_get[0].place(x = 250, y=100)
    key_place = Label(top1, width=14, text = '输入16进制秘钥:', height=1, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    key_place.place(x = 50, y = 100)

    bash = Label(top1, width=60, height=2, relief='sunken', bd='2',
                 fg='red', font=('黑体', 11, 'bold'))
    bash.config(text='等待设置完成')
    bash.place(x=150, y=200)

    def decode():
        bash.config(text = '解密原文为0x' + aes_decode(cipher_get[0].get(), key_get[0].get()))

    sub = Button(top1, width=10, text='开始解密', relief='sunken', bd='2', font=('黑体', 10, 'bold'), command=decode)
    sub.place(x=10, y=200)

    top1.mainloop()

"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现ctr GUI加密界面
 ****************************************************************************************"""


def encode_ctr():

    top1 = Toplevel()
    path = [1] * 2
    path[0] = os.getcwd()
    path[1] = os.getcwd()
    top1.geometry('800x840')
    encode_path = [None]

    encode_frame = Frame(top1)
    encode_frame.place(x = 25, y = 70)
    encode_place = Label(top1, width=75, height=2, relief='sunken', bd='2',
                           fg='blue',font=('黑体',11,'bold'))
    encode_place.config(text ='明文文件路径位置:' + path[0])
    encode_place.place(x = 10, y = 20)
##########################################################################
    encode_file = Label(top1, width=75, height=2, relief='sunken', bd='2',
                         fg='red', font=('黑体', 11, 'bold'))
    encode_file.config(text='请选择非目录性质的文件')
    encode_file.place(x=10, y=320)
##########################################################################

    encode_dir = Listbox(encode_frame, width=57, height=10, relief='sunken', bd='2', font=('黑体',14,'bold'))
    encode_srollbar = Scrollbar(encode_frame)
    encode_srollbar.pack(side = RIGHT, fill = Y)

############################################################################
    # 获取当前目录下所有文件
    def encode_context():
        all = ['{:s}:返回上一级目录'.format('目录')]
        for file in os.listdir(path[0]):
            if(os.path.isdir(path[0] + '/' + file)):
                all.append('{:s}:{:s}'.format('目录', file))
            else:
                all.append('{:s}:{:s}'.format('非目录', file))
        all[1:].sort()
        return all


    encode_dir['yscrollcommand'] = encode_srollbar.set
    encode_srollbar['command'] = encode_dir.yview

    for i in encode_context():
        encode_dir.insert(END, i)

    #   获取用户点击的文件,并判断相应文件
    def encode_event(event):
        tmp = encode_dir.get(encode_dir.curselection())
        tmp = tmp.split(':')
        if(tmp[0] == '非目录'):
            encode_file.config(text = '选择的文件为:' + path[0] + '\\' + tmp[1])
            encode_path[0] = path[0] + '\\' + tmp[1]
        else:
            encode_path[0] = None
            encode_file.config(text='请选择非目录性质的文件')
            if(tmp[1] == '返回上一级目录'):
                os.chdir('\..')
                path[0] = os.getcwd()
            else:
                path[0] = path[0] + '/' + tmp[1]
                os.chdir(path[0])

            encode_place.config(text='路径位置:' + path[0])

            encode_dir.delete(0, END)
            for i in encode_context():
                encode_dir.insert(END, i)

    encode_dir.bind('<Double-Button-1>', encode_event)
    encode_dir.pack()


##############################################################################选择加密的文件


    decode_frame = Frame(top1)
    decode_frame.place(x=25, y=420)
    decode_place = Label(top1, width=75, height=2, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    decode_place.config(text='密文文件路径位置:' + path[0])
    decode_place.place(x=10, y=370)
    ##########################################################################
    decode_file = Label(top1, width=15, height=2, relief='sunken', bd='2',
                        fg='red', font=('黑体', 11, 'bold'))
    decode_file.config(text='请输入文件名称:')
    decode_file.place(x=10, y=670)
    ##########################################################################

    decode_dir = Listbox(decode_frame, width=57, height=10, relief='sunken', bd='2', font=('黑体', 14, 'bold'))
    decode_srollbar = Scrollbar(decode_frame)
    decode_srollbar.pack(side=RIGHT, fill=Y)
    decode_get = [Entry(top1, width = 40, font=('黑体', 14, 'bold'))]
    decode_get[0].place(x = 200, y = 680)

    key_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    key_get[0].place(x = 250, y=720)
    key_place = Label(top1, width=14, text = '输入16进制秘钥:', height=1, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    key_place.place(x = 50, y = 720)
    t_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    t_get[0].place(x=250, y=750)
    t_place = Label(top1, width=15, text = '请输入十进制的t:', height=1, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    t_place.place(x=50, y=750)
    ############################################################################

    # 获取当前目录下所有文件
    def decode_context():
        all = ['{:s}:返回上一级目录'.format('目录')]
        for file in os.listdir(path[1]):
            if(os.path.isdir(path[1] + '/' + file)):
                all.append('{:s}:{:s}'.format('目录', file))
            else:
                all.append('{:s}:{:s}'.format('非目录', file))
        all[1:].sort()
        return all

    decode_path = [None]
    decode_dir['yscrollcommand'] = decode_srollbar.set
    decode_srollbar['command'] = decode_dir.yview

    for i in decode_context():
        decode_dir.insert(END, i)

    #   获取用户点击的文件,并判断相应文件
    def decode_event(event):
        tmp = decode_dir.get(decode_dir.curselection())
        tmp = tmp.split(':')
        if(tmp[1] == '非目录'):
            decode_file.config(text = '选择的文件为:' + path[1] + '\\' + tmp[1])
        else:
            decode_path[0] = None
            decode_file.config(text='请输入加密后文件名称')
            if(tmp[1] == '返回上一级目录'):
                os.chdir('\..')
                path[1] = os.getcwd()
            else:
                path[1] = path[1] + '\\' + tmp[1]
                os.chdir(path[1])
            decode_place.config(text='路径位置:' + path[1])

            decode_dir.delete(0, END)
            for i in decode_context():
                decode_dir.insert(END, i)

    decode_dir.bind('<Double-Button-1>', decode_event)
    decode_dir.pack()

    bash = Label(top1, width=60, height=2, relief='sunken', bd='2',
                 fg='red', font=('黑体', 11, 'bold'))
    bash.config(text='等待设置完成')
    bash.place(x=150, y=790)


    def encode():
        if(decode_get[0] in os.listdir(path[1])):
            bash.config(text = '加密或解密文件已存在')
        else:
            ctr(encode_path[0], path[1] + '\\' + decode_get[0].get(),
                key_get[0].get(), int(t_get[0].get()))
            bash.config(text = '加密完成')

    encode_sub = Button(top1, width=10, text='开始加密', relief='sunken', bd='2', font=('黑体', 10, 'bold'), command=encode)
    encode_sub.place(x=10, y=795)


    top1.mainloop()




"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现位ctr GUI解密界面
 ****************************************************************************************"""

def decode_ctr():

    top1 = Toplevel()
    path = [1] * 2
    path[0] = os.getcwd()
    path[1] = os.getcwd()
    top1.geometry('800x840')
    encode_path = [None]

    encode_frame = Frame(top1)
    encode_frame.place(x = 25, y = 70)
    encode_place = Label(top1, width=75, height=2, relief='sunken', bd='2',
                           fg='blue',font=('黑体',11,'bold'))
    encode_place.config(text ='密文件路径位置:' + path[0])
    encode_place.place(x = 10, y = 20)
##########################################################################
    encode_file = Label(top1, width=75, height=2, relief='sunken', bd='2',
                         fg='red', font=('黑体', 11, 'bold'))
    encode_file.config(text='请选择非目录性质的文件')
    encode_file.place(x=10, y=320)
##########################################################################

    encode_dir = Listbox(encode_frame, width=57, height=10, relief='sunken', bd='2', font=('黑体',14,'bold'))
    encode_srollbar = Scrollbar(encode_frame)
    encode_srollbar.pack(side = RIGHT, fill = Y)

############################################################################
    # 获取当前目录下所有文件
    def encode_context():
        all = ['{:s}:返回上一级目录'.format('目录')]
        for file in os.listdir(path[0]):
            if(os.path.isdir(path[0] + '/' + file)):
                all.append('{:s}:{:s}'.format('目录', file))
            else:
                all.append('{:s}:{:s}'.format('非目录', file))
        all[1:].sort()
        return all


    encode_dir['yscrollcommand'] = encode_srollbar.set
    encode_srollbar['command'] = encode_dir.yview

    for i in encode_context():
        encode_dir.insert(END, i)

    #   获取用户点击的文件,并判断相应文件
    def encode_event(event):
        tmp = encode_dir.get(encode_dir.curselection())
        tmp = tmp.split(':')
        if(tmp[0] == '非目录'):
            encode_file.config(text = '选择的文件为:' + path[0] + '\\' + tmp[1])
            encode_path[0] = path[0] + '\\' + tmp[1]
        else:
            encode_path[0] = None
            encode_file.config(text='请选择非目录性质的文件')
            if(tmp[1] == '返回上一级目录'):
                os.chdir('\..')
                path[0] = os.getcwd()
            else:
                path[0] = path[0] + '/' + tmp[1]
                os.chdir(path[0])

            encode_place.config(text='路径位置:' + path[0])

            encode_dir.delete(0, END)
            for i in encode_context():
                encode_dir.insert(END, i)

    encode_dir.bind('<Double-Button-1>', encode_event)
    encode_dir.pack()


##############################################################################选择加密的文件


    decode_frame = Frame(top1)
    decode_frame.place(x=25, y=420)
    decode_place = Label(top1, width=75, height=2, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    decode_place.config(text='明文文件路径位置:' + path[0])
    decode_place.place(x=10, y=370)
    ##########################################################################
    decode_file = Label(top1, width=15, height=2, relief='sunken', bd='2',
                        fg='red', font=('黑体', 11, 'bold'))
    decode_file.config(text='请输入文件名称:')
    decode_file.place(x=10, y=670)
    ##########################################################################

    decode_dir = Listbox(decode_frame, width=57, height=10, relief='sunken', bd='2', font=('黑体', 14, 'bold'))
    decode_srollbar = Scrollbar(decode_frame)
    decode_srollbar.pack(side=RIGHT, fill=Y)
    decode_get = [Entry(top1, width = 40, font=('黑体', 14, 'bold'))]
    decode_get[0].place(x = 200, y = 680)

    key_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    key_get[0].place(x = 250, y=720)
    key_place = Label(top1, width=14, text = '输入16进制秘钥:', height=1, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    key_place.place(x = 50, y = 720)
    t_get = [Entry(top1, width=34, font=('黑体', 14, 'bold'))]
    t_get[0].place(x=250, y=750)
    t_place = Label(top1, width=15, text = '请输入十进制的t:', height=1, relief='sunken', bd='2',
                         fg='blue', font=('黑体', 11, 'bold'))
    t_place.place(x=50, y=750)
    ############################################################################

    # 获取当前目录下所有文件
    def decode_context():
        all = ['{:s}:返回上一级目录'.format('目录')]
        for file in os.listdir(path[1]):
            if(os.path.isdir(path[1] + '/' + file)):
                all.append('{:s}:{:s}'.format('目录', file))
            else:
                all.append('{:s}:{:s}'.format('非目录', file))
        all[1:].sort()
        return all

    decode_path = [None]
    decode_dir['yscrollcommand'] = decode_srollbar.set
    decode_srollbar['command'] = decode_dir.yview

    for i in decode_context():
        decode_dir.insert(END, i)

    #   获取用户点击的文件,并判断相应文件
    def decode_event(event):
        tmp = decode_dir.get(decode_dir.curselection())
        tmp = tmp.split(':')
        if(tmp[1] == '非目录'):
            decode_file.config(text = '选择的文件为:' + path[1] + '\\' + tmp[1])
        else:
            decode_path[0] = None
            decode_file.config(text='请输入加密后文件名称')
            if(tmp[1] == '返回上一级目录'):
                os.chdir('\..')
                path[1] = os.getcwd()
            else:
                path[1] = path[1] + '\\' + tmp[1]
                os.chdir(path[1])
            decode_place.config(text='路径位置:' + path[1])

            decode_dir.delete(0, END)
            for i in decode_context():
                decode_dir.insert(END, i)

    decode_dir.bind('<Double-Button-1>', decode_event)
    decode_dir.pack()

    bash = Label(top1, width=60, height=2, relief='sunken', bd='2',
                 fg='red', font=('黑体', 11, 'bold'))
    bash.config(text='等待设置完成')
    bash.place(x=150, y=790)


    def decode():
        if(decode_get[0] in os.listdir(path[1])):
            bash.config(text = '加密或解密文件已存在')
        else:
            ctr(encode_path[0], path[1] + '\\' + decode_get[0].get(),
                key_get[0].get(), int(t_get[0].get()))
            bash.config(text = '解密完成')

    decode_sub = Button(top1, width=10, text='开始解密', relief='sunken', bd='2', font=('黑体', 10, 'bold'), command=decode)
    decode_sub.place(x=10, y=795)


    top1.mainloop()
if(__name__ == '__main__'):
    window()

"""****************************************************************************************
 ** Description:        key = 0f1571c947d9e8590cb7add6af7f6798
                        t   = 123456
                        
                        
                        明文：0123456789abcdeffedcba9876543210
                        密钥：0f1571c947d9e8590cb7add6af7f6798
                        密文：ff0b844a0853bf7c6934ab4364148fb9
 ****************************************************************************************"""