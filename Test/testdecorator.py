class decorators():
    def log_function(func):
        def wrapper(*args, **kwargs):
            print(f"{func} function, argument {args} start!")
            ret = func(*args, **kwargs)
            print(f"{func} function, argument {args} completed!")
            return ret
        return wrapper
    # 装饰器定义之后加上下面这行代码，即可实现类内外装饰器使用
    log_function = staticmethod(log_function)

    # 类中定义的装饰器装饰类中定义的函数
    @log_function
    def fib1(self):
        print("Process fib1 function")

# 通过类调用装饰器来装饰类外的函数
@decorators.log_function
def fib2():
    print("Process fib2 function")

# 通过类对象调用装饰器来装饰类外的函数
dec = decorators()
@dec.log_function
def fib3():
    print("Process fib3 function")

dd = decorators()
dd.fib1()
fib2()
fib3()