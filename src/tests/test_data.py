#!/usr/bin/env python
from pyplus.data import dataobject, DataObjectMixin
from pytest import raises


@dataobject("index", "name", "value")
class Object1(object):
    def __init__(self, index, name, value):
        self.index = index
        self.name = name
        self.value = value

    def __eq__(self, other):
        try:
            return self.index == other.index and self.name == other.name and self.value == other.value
        except AttributeError:
            return False


@dataobject("index", "name", "value")
class Object2(DataObjectMixin):

    def __init__(self, index, name, value):
        self.index = index
        self.name = name
        self.value = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.index == other.index and self.name == other.name and self.value == other.value
        else:
            return False


def test_dataobject():
    object1 = Object1(1, "object", 1.1)
    assert object1 == Object1.from_list([1, "object", 1.1])
    assert object1 == object1.from_dict({"index": 1, "name": "object", "value": 1.1})

    with raises(AttributeError):
        Object1.from_line("")

    with raises(AttributeError):
        object1.from_line("")

    object2 = Object2(1, "object", 1.1)
    assert object2 == Object2.from_list([1, "object", 1.1])
    assert object2 == object2.from_dict({"index": 1, "name": "object", "value": 1.1})

    with raises(AttributeError):
        Object2.from_line("")

    with raises(AttributeError):
        object2.from_line("")


if __name__ == "__main__":
    test_dataobject()
