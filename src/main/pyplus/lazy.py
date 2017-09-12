#!/usr/bin/env python
from copy import deepcopy as _deepcopy
from os import name as _name
from pathlib import Path as _Path, PosixPath as _PosixPath, WindowsPath as _WindowsPath


class LazyObject(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __copy__(self):
        return self.__class__(**self.__dict__)

    def __deepcopy__(self, memo):
        kwargs = {key: _deepcopy(value) for key, value in self.__dict__.items()}
        return self.__class__(**kwargs)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, key))


class ImmutableLazyObject(LazyObject):

    def __setattr__(self, key, value):
        raise AttributeError("can't set attribute '%s' objects are immutable" % type(self).__name__)


class LazyPath(_Path):

    def __new__(cls, *args, **kwargs):
        if cls is LazyPath:
            cls = LazyWindowsPath if _name == "nt" else LazyPosixPath

        self = cls._from_parts(args, init=False)
        if not self._flavour.is_supported:
            raise NotImplementedError("cannot instantiate %r on your system" % (cls.__name__,))

        self._init()
        return self

    def read(self, mode="r", buffering=-1, encoding=None, errors=None, newline=None):
        if self.exists():
            return self.open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)
        else:
            return None

    def write(self, mode="w", buffering=-1, encoding=None, errors=None, newline=None):
        parent = _Path(self.parent)

        if not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)

        if not self.exists():
            self.touch()

        return self.open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)


class LazyPosixPath(LazyPath, _PosixPath):
    pass


class LazyWindowsPath(LazyPath, _WindowsPath):
    pass
