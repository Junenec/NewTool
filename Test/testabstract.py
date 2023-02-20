from abc import abstractmethod, ABCMeta, ABC

class Generator1():
    @abstractmethod
    def generator(self):
        raise NotImplementedError("generator method for Generator1 not implemented")
    @abstractmethod
    def production(self):
        raise NotImplementedError("production method for Generator1 not implemented")

class Generator2(ABC):
    @abstractmethod
    def generator(self):
        raise NotImplementedError("generator method for Generator2 not implemented")
    @abstractmethod
    def production(self):
        raise NotImplementedError("production method for Generator2 not implemented")

class FinalGenerator(Generator1):
    def generator(self):
        print("ABC")

gen1 = FinalGenerator()
gen1.generator()
gen1.production()