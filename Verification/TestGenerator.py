import time
def fibonacci(i):
    a, b = 0, 1
    count = 0
    print("Start to execute fibonacci")
    while True:
        if count > i:
            break
        yield a + b
        print("In Progress")
        a, b = b, a + b
        count += 1


# 1. 创建fibonacci生成器
gen = fibonacci(250)
print(list(gen))
gen2 = fibonacci(250)
print(tuple(gen2))
