
# time1 = time.perf_counter()
# nums = []
# for n in range(1000000):
#     nums.append(n**2)
# time2 = time.perf_counter()
# print(time2 - time1)

import time
class Timer:
    def __init__(self):
        self.elapsed = 0
    def __enter__(self):
       self.start = time.perf_counter()
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = time.perf_counter()
        self.elapsed = self.stop - self.start
        print(self.elapsed)

with Timer() as timer:
    nums = []
    for n in range(1000000):
        nums.append(n**2)