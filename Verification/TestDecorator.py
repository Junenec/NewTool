from functools import wraps
import types

class animal:
    def __init__(self, func):
        self.func = func

    @wraps
    def __call__(self, *args, **kwargs):
        print('working here')
        res = self.func(*args, **kwargs)
        return res

        # 注意要写这个__get__，否则会报错
        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                return types.MethodType(self, instance)

@animal
def test(name, kind):
    word = '{} belongs to {}'.format(name, kind)
    return word


A = test('cow', 'mammals')
print(type(test))
print(A)