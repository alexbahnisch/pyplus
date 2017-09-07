#!/usr/bin/env python
from past.builtins import basestring


def assert_exception(method, exception=Exception, message=None):
    assert callable(method)
    assert issubclass(exception, BaseException)
    assert isinstance(message, basestring) or message is None

    try:
        method()
        raise AssertionError("'%s' method did not raise '%s' exception" % (method.__name__, exception.__name__))

    except exception as exc:
        if message is not None:
            if str(exc) != message:
                raise AssertionError("'%s' method did not raise the correct exception message")

    except BaseException as exc:
        raise AssertionError("'%s' method raised a '%s' exception instead of the required '%s' exception" %
                             (method.__name__, exc.__class__.__name__, exception.__name__))
