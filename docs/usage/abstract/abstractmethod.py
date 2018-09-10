from pyplus.abstract import abstractmethod


class AbstractClass:
    @abstractmethod
    def method(self):
        pass


abstract_instance = AbstractClass()
abstract_instance.method()


# -> AttributeError: abstract method 'method' has not been overridden for
# 'AbstractClass' class

class BadClass(AbstractClass):
    pass


bad_instance = BadClass()
bad_instance.method()


# -> AttributeError: abstract method 'method' has not been overridden for
# 'BadClass' class

class GoodClass(AbstractClass):
    def method(self):
        return "Hello world!"


good_instance = GoodClass()
good_instance.method()
# -> 'Hello world!'
