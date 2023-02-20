"""Prepare a python file to co"""
import base64


def createImage(self, file_name="E+H_Logo.gif"):
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