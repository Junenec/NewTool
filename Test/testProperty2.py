class Person():
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def method_with_property(self):
        return self.__name

    def method_without_property(self):
        return self.__age

if __name__ == '__main__':
    Jasmine = Person("Jasmine", 22)
    print(Jasmine.method_without_property())  # Jasmine
    Jasmine.__Person__age = 20
    print(Jasmine.method_without_property())  # Jasmine
