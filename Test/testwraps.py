import time

def run_time(func):
    def wrapper(*args, **kwargs):
        """运行时间装饰器"""
        time1 = time.time()
        func(*args, **kwargs)
        time2 = time.time()
        cost_time = time2 - time1
        return f"运行函数划分了{cost_time}秒"
    return wrapper

@run_time
def test():
    """测试"""
    print([i for i in range(10000) if i%200==0])

if __name__ == '__main__':
    print(test.__name__) # wrapper
    print(test.__doc__) # 运行时间装饰器