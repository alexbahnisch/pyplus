from pyplus.abstract import abstractclassmethod


class AbstractClass:
    @abstractclassmethod
    def class_method(cls):
        pass


AbstractClass.class_method()
# -> AttributeError: abstract class method 'class_method' has not been 
# overridden for 'AbstractClass' class


class BadClass(AbstractClass):
    pass


BadClass.class_method()
# -> AttributeError: abstract class method 'class_method' has not been 
# overridden 'BadClass' class


class GoodClass(AbstractClass):
    @classmethod
    def class_method(cls):
        return "Hello world!"


GoodClass.class_method()
# -> 'Hello world!'
