class Person():
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def __str__(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise ValueError("Age must be a number!")
        if value < 0 or value >200:
            raise ValueError("Age should be between 0 and 200 years old!")
        self.__age = value

if __name__ == '__main__':
    Jasmine = Person("Jasmine", 22)
    print(Jasmine.age)
    Jasmine.age = 30
    print(Jasmine.age)
