"""****************************************************************************************
 ** FileName:        gui.py
 ** Author:          Jiawei Hawkins
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现最终的GUI界面
 ****************************************************************************************"""

from ctr_mode import ctr
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
           command=lambda: decode_ctr).place(x=290, y=630)
    root.mainloop()

"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现128bit GUI加密界面
 ****************************************************************************************"""


def encode_128():
    top1 = Toplevel()
    top1.geometry('700x600')




"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现位128bit GUI解密界面
 ****************************************************************************************"""

def decode_128():
    top1 = Toplevel()
    top1.geometry('700x600')


"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现ctr GUI加密界面
 ****************************************************************************************"""


def encode_ctr():

    # top1 = Toplevel()
    path = [1]
    path[0] = os.getcwd()
    top1 = Tk()
    top1.geometry('700x700')
    encode_path = [None]

    encode_frame = Frame(top1)
    encode_frame.place(x = 25, y = 70)
    encode_place = Label(top1, width=75, height=2, relief='sunken', bd='2',
                           fg='blue',font=('黑体',11,'bold'))
    encode_place.config(text ='路径位置:' + path[0])
    encode_place.place(x = 10, y = 20)
##########################################################################
    encode_file = Label(top1, width=75, height=2, relief='sunken', bd='2',
                         fg='red', font=('黑体', 11, 'bold'))
    encode_file.config(text='请选择非目录性质的文件')
    encode_file.place(x=10, y=290)
##########################################################################

    encode_dir = Listbox(encode_frame, width=57, height=10, relief='sunken', bd='2', font=('黑体',14,'bold'))
    encode_srollbar = Scrollbar(encode_frame)
    encode_srollbar.pack(side = RIGHT, fill = Y)

    # 获取当前目录下所有文件
    def get_context():
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

    for i in get_context():
        encode_dir.insert(END, i)

    #   获取用户点击的文件,并判断相应文件
    def encode_event(event):
        tmp = encode_dir.get(encode_dir.curselection())
        tmp = tmp.split(':')
        if(tmp[0] == '非目录'):
            encode_file.config(text = '选择的文件为:' + path[0] + '\\' + tmp[1])
        else:
            encode_path[0] = None
            encode_file.config(text='请选择非目录性质的文件')
            if(tmp[1] == '返回上一级目录'):
                os.chdir('\..')
                path[0] = os.getcwd()
            else:
                path[0] = path[0] + '\\' + tmp[1]
                os.chdir(path[0])
            encode_place.config(text='路径位置:' + path[0])

            encode_dir.delete(0, END)
            for i in get_context():
                encode_dir.insert(END, i)

    encode_dir.bind('<Double-Button-1>', encode_event)

    encode_dir.pack()

    top1.mainloop()




"""****************************************************************************************
 ** Date:            2019-04-14 星期天 17:54:32
 ** Description:     实现位ctr GUI解密界面
 ****************************************************************************************"""

def decode_ctr():
    top1 = Toplevel()
    top1.geometry('700x600')

#window()
encode_ctr()