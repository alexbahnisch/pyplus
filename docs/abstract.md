A collection of lazy abstract decorators that will only raise an exception when the decorated method is called before
being overridden, instead of on initiation of a subclass instance.

## abstractclassmethod

A lazy alternative to the `abc.abstractclassmethod(method)`.

#### parameters:
* `method` - *{classmethod}* an empty class method

#### return 
* *{classmethod}* an abstract class method that will raise an exception when called

### usage
```python
from pyplus.abstract import abstractclassmethod

class AbstractClass:
    @abstractclassmethod
    def class_method(cls):
        pass

AbstractClass.class_method()

"""
AttributeError: abstract class method 'class_method' has not been overridden 
for 'AbstractClass' class
"""

class BadClass(AbstractClass):
    pass

BadClass.class_method()

"""
AttributeError: abstract class method 'class_method' has not been overridden 
for 'BadClass' class
"""

class GoodClass(AbstractClass):
    @classmethod
    def class_method(cls):
        return "Hello world!"
    

GoodClass.class_method()

"""
'Hello world!'
"""

```


## abstractmethod

A lazy alternative to the `abc.abstractmethod(method)`.

#### parameters:
* `method` - *{method}* an empty method

#### return 
* *{method}* an abstract method that will raise an exception when called

### usage
```python
from pyplus.abstract import abstractmethod

class AbstractClass:
    @abstractmethod
    def method(self):
        pass

abstract_instance = AbstractClass()
abstract_instance.method()

"""
AttributeError: abstract method 'method' has not been overridden for 
'AbstractClass' class
"""

class BadClass(AbstractClass):
    pass

bad_instance = BadClass()
bad_instance.method()

"""
AttributeError: abstract method 'method' has not been overridden for 
'BadClass' class
"""

class GoodClass(AbstractClass):
    def method(self):
        return "Hello world!"
    

good_instance = GoodClass()
good_instance.method()

"""
'Hello world!'
"""

```
