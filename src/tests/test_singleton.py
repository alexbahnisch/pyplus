#!/usr/bin/env python
from pyplus.singleton import singleton


@singleton
class Singleton:
    def __init__(self, param):
        self.param = param


def test_singleton():
    param1 = [1, 2, 3]
    param2 = [1, 2, 3]
    singleton1 = Singleton(param1)
    singleton2 = Singleton(param2)

    assert param1 == param2
    assert param1 is not param2
    assert singleton1 is singleton2
    assert singleton1.param is singleton2.param
