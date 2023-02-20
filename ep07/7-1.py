# from ep07.DemoClass import Cat


class Cat:
    """
    这是一只猫的类
    """
    def __init__(self, name):
        self.name = name
        print("我是一只猫，我的名字叫{}".format(self.name))

    def __del__(self):
        print("{}被系统回收啦".format(self.name))


cat = Cat("Chris")


# 输出： 我是一只猫，我的名字叫Chris