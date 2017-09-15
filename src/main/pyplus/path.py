#!/usr/bin/env python
from os import name as _name
from pathlib import Path as _Path, PosixPath as _PosixPath, WindowsPath as _WindowsPath
from tempfile import TemporaryDirectory as _TemporaryDirectory


# noinspection PyAbstractClass
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


# noinspection PyAbstractClass
class LazyPosixPath(LazyPath, _PosixPath):
    pass


# noinspection PyAbstractClass
class LazyWindowsPath(LazyPath, _WindowsPath):
    pass


# noinspection PyShadowingBuiltins
class LazyTempDir(_TemporaryDirectory):

    def __init__(self, suffix=None, prefix=None, dir=None):
        super().__init__(suffix, prefix, dir)

    def __enter__(self):
        return LazyPath(self.name)

    def __str__(self):
        return self.name
