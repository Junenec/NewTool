def testfunc(*args, **kwargs):
    for i in args:
        print(i)
    for i in kwargs:
        print(i, kwargs[i])

testfunc(1,2,3,a=2,b=4)