class testException(Exception):
    pass


list = [1, 33, 44]
for i in list:
    print(i)
    if i == 33:
        raise testException("i should not be 33")