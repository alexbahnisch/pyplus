#!/usr/bin/env python
from datetime import timedelta

from pyplus.decorators import *
from pytest import raises


class Callable:
    def __call__(self, *args, **kwargs):
        pass


class TimerTest:
    def __init__(self):
        self._calls = 0

    def __call__(self, arg):
        if self._calls == 0:
            assert isinstance(arg, timedelta)
        elif self._calls == 1:
            assert "starting" in arg
        elif self._calls == 2:
            assert "finished" in arg and "completed in" in arg
        self._calls += 1


def func(*args, **kwargs):
    pass


@parser
def parse(string):
    return string


@spliter
def split(string):
    return [string]


def timer_callback(arg):
    assert isinstance(arg, timedelta)


def timer_plus_callback(arg):
    assert isinstance(arg, str)


def test_decorator():
    call = decorator(Callable())
    assert callable(call)

    cls = decorator(Callable)
    assert callable(cls)

    fun = decorator(func)
    assert callable(fun)

    with raises(TypeError, message="'NoneType' object is not callable"):
        decorator(None)


def test_parser():
    assert "string" == parse("string")
    assert b"string" == parse(b"string")
    assert u"string" == parse(u"string")

    with raises(TypeError, message="'NoneType' object is not a string"):
        parse(None)


def test_spliter():
    assert ["string"] == split("string")
    assert [b"string"] == split(b"string")
    assert [u"string"] == split(u"string")
    assert [1] == split(1)
    assert [1.5] == split(1.5)
    assert [] == split(None)

    with raises(TypeError, message="'type' object is not a string"):
        split(object)


def test_timer_plus():
    timer_test = TimerTest()
    test_timer = Timer(logger=timer_test)
    test_timer(func)()

    test_timer.disable()
    assert func == test_timer(func)
    assert func == test_timer.plus(func)

    test_timer.enable()
    test_timer.plus(func)()
