"""Implement the UI designer for Calibration Tool"""
from tkinter import *
from base64 import b64decode
import base64

class UIApplication(Frame):
    def __init__(self, master = Frame):
        super().__init__(master)
        self.pack()
        self.createWidget()


    def createWidget(self):
        pass

    def __createImage(self, file_name = "E+H_Logo.gif"):
        write_data = []
        picture_data = 'EH_Logo'
        logo_py_name = "logo"
        # 从指定文件中读取数据，并将数据写入write_data中
        pic_data = open(file_name, 'rb')
        b64str = base64.b64encode(pic_data.read())
        pic_data.close()
        write_data.append('%s = "%s"\n' % (picture_data, b64str.decode()))
        # 将变量logo写入logo.py
        f = open('%s.py' % logo_py_name, 'w+')
        for data in write_data:
            f.write(data)
        f.close()
        #
        #
        # picture_name = "E+H_Logo.gif"
        # py_name = 'memory_pic'
        # # filename = picture_name.replace('.', '_')
        # # open_pic = open("%s" % picture_name, 'rb')
        # open_pic = open("%s" % picture_name, 'rb')
        # b64str = base64.b64encode(open_pic.read())
        # open_pic.close()
        # # 注意这边b64str一定要加上.decode()
        # write_data.append('%s = "%s"\n' % (picture_name, b64str.decode()))
        # print(write_data)
        # f = open('%s.py' % py_name, 'w+')
        # for data in write_data:
        #     f.write(data)
        # f.close()

class MainUI():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('800x700')
        self.root.title("Remote Calibration - Copyright 2020 恩德斯豪斯分析仪器（苏州）有限公司")
        self.app = UIApplication(master = self.root)

    def initialize(self):
        self.root.mainloop()

if __name__ == '__main__':
    MainUI().app.createImage()
    # EH_Logo_gif = ''
    # image = open('EH_Logo.gif','wb')
    # image.write(b64decode(EH_Logo_gif))
    # print(EH_Logo_gif)

