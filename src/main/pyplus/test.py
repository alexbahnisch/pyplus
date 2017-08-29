#!/usr/bin/env python


def assert_exception(method, exception=Exception, message=None):
    assert callable(method)

    try:
        method()
        assert False
    except exception as exc:
        if message is not None:
            assert str(exc) == message
        assert True


def bad():
    a = float("hello")


if __name__ == "__main__":
    assert_exception(bad, ValueError, "could not convert string to float: 'hello'")
