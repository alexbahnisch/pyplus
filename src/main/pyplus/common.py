from sys import version_info as _version


def isintlike(obj):
    try:
        int(obj)
        return True
    except (TypeError, ValueError):
        return False


def isiterable(obj):
    return hasattr(obj, "__iter__") or isinstance(obj, str)


def islistlike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and hasattr(obj, "__setitem__") and isiterable(obj)


def ispair(obj):
    return hasattr(obj, "__len__") and len(obj) == 2 and isiterable(obj)


def ismappable(obj):
    return isinstance(obj, dict) or (isiterable(obj) and all(ispair(item) for item in obj))


def issequence(obj):
    return hasattr(obj, "__len__") and isiterable(obj)


def istuplike(obj):
    return hasattr(obj, "__len__") and hasattr(obj, "__getitem__") and isiterable(obj)


def iterable(obj):
    if isiterable(obj):
        return obj
    else:
        return [obj]
