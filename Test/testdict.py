class Teacher:
    def __init__(self, name, age):
        self.name = name
        self.age = age

Feyman = Teacher("Feyman", 42)

# 通过类名调用__dict__
print(Teacher.__dict__) # {'__module__': '__main__', '__init__': <function Teacher.__init__ at 0x0000014AC7B8A290>, '__dict__': <attribute '__dict__' of 'Teacher' objects>, '__weakref__': <attribute '__weakref__' of 'Teacher' objects>, '__doc__': None}
print(Feyman.__dict__) # {'name': 'Feyman', 'age': 42}
