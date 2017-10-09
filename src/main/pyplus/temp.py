#!/usr/bin/env python
from shutil import rmtree as _rmtree
from tempfile import mkdtemp as _mkdtemp, mkstemp as _mkstemp

from .path import LazyPath as _LazyPath


# noinspection PyShadowingBuiltins
class LazyTempDir:
    __PATH__ = _LazyPath

    def __init__(self, suffix=None, prefix=None, dir=None):
        self._path = self.__PATH__(_mkdtemp(suffix, prefix, dir))

    def __enter__(self):
        return self.path

    def __exit__(self, exc, value, tb):
        self.delete()

    def __repr__(self):
        return repr(self._path)

    def __str__(self):
        return self.name

    def delete(self):
        if self.path.exists():
            _rmtree(self.name)

    @property
    def name(self):
        return str(self._path)

    @property
    def path(self):
        return self._path


# noinspection PyShadowingBuiltins
class LazyTempFile:
    __PATH__ = _LazyPath

    def __init__(self, suffix=None, prefix=None, dir=None):
        self._path = self.__PATH__(_mkstemp(suffix, prefix, dir))

    def __enter__(self):
        return self.path

    def __exit__(self, exc, value, tb):
        self.delete()

    def __repr__(self):
        return repr(self._path)

    def __str__(self):
        return self.name

    def delete(self):
        if self.path.exists():
            _rmtree(self.name)

    @property
    def name(self):
        return str(self._path)

    @property
    def path(self):
        return self._path
