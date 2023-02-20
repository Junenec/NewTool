import colorsys
from PIL import Image

def changeColor():
    # 1. 指定图像路径
    filename = 'C:\\Work\\NewTool\\Verification\\pic.jpg'
    # 2. 读入图片，转换为RGB色值
    img = Image.open(filename).convert('RGB')
    width, height = img.size
    img_array = img.load()
    # 3. 将颜色范围内的色点改为指定颜色
    for w in range(0,width):
        for h in range(0,height):
            color_dot = img_array[w,h]
            if((color_dot[0]>30 and color_dot[0]<60) and (color_dot[1]>60 and color_dot[1]<100)  and (color_dot[2]>100 and color_dot[2]<170)):
                img_array[w, h] = (255, 255, 255)
    img.save('C:\\Work\\NewTool\\Verification\\snow.jpg')

def transparentPicture():
    # 1. 指定图像路径
    filename = 'as777.jpg'
    # 2. 读入图片，转换为RGB色值
    img = Image.open(filename).convert('RGBA')
    width, height = img.size
    # 3. 将颜色范围内的色点改为透明色
    for w in range(0,width):
        for h in range(0,height):
            dot = img.getpixel((w, h))
            #print(dot)
            if dot[0]>40 and dot[0]<60 and dot[1]>50 and dot[1]<70 and dot[2]>60 and dot[2]<90:
                dot = (dot[:-1] + (0,))
                img.putpixel((w, h), dot)
            elif dot[0] >= 60 and dot[0] < 80 and dot[1] > 60 and dot[1] < 80 and dot[2] > 60 and dot[2] < 80:
                dot = (dot[:-1] + (0,))
                img.putpixel((w, h), dot)
    # 4. 保存为新的图片
    img.save('asqqq.png')



if __name__ == '__main__':
    transparentPicture()