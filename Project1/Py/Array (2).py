'''*****************************************************************************************
   ** FileName:        test.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-04 星期一 17:59:46
   ** Description:     
   **************************************************************************************'''

'''*****************************************************************************************
   ** FileName:        arrya.py
   ** Author:          Jiawei Hawkins
   ** Date:            2019-03-03 星期日 23:51:37
   ** Description:     硬盘当内存
   **************************************************************************************'''

import os

const = 5


class array:                                        # 和列表操作基本相似
                                                    # 但内存可以足够大
    num = 0
    table = []
    if os.path.exists("storage.txt"):
        os.remove("storage.txt")
    file = open("storage.txt", "wb+")

    def set(self, num, value):
        self.num = num
        if (num <= const):
            self.table = [value] * num
        else:
            self.table = [value] * const
            self.file.write(bytes(str(value), "utf-8") * (num - const))

    def append(self, value):
        self.num = self.num + 1
        if (self.num <= const):
            self.table.append(value)
        else:
            self.file.seek(0, 2)
            self.file.write(bytes(str(value), "utf-8"))
            self.file.flush()

    def write(self, place, value):
        if (place < const):
            self.table[place] = value
        elif (place < self.num):
            self.file.seek(place - const, 0)
            self.file.write(bytes(str(value), "utf-8"))
            self.file.flush()
        else:
            print("Error: Out of Index")

    def read(self, place):
        if (place < const):
            return int(self.table[place])
        elif (place < self.num):
            self.file.seek(place - const, 0)
            return int(self.file.read(1))
        else:
            print("Error: Out of Index")
            return None

    def delete(self):
        self.file.close()
        os.remove("storage.txt")


test = array()
test.set(10,1)
test.write(5, None)
for i in range(0, 10):
    print( test.read(i))
test.delete()