#!/usr/bin/env python
from os import remove as _remove
from shutil import rmtree as _rmtree
from tempfile import mkdtemp as _mkdtemp, mkstemp as _mkstemp

from .path import LazyPath as _LazyPath


# noinspection PyShadowingBuiltins
class _LazyTempMixin:
    __PATH__ = _LazyPath
    __TEMP__ = None

    def __init__(self, suffix=None, prefix=None, dir=None):
        self._path = self.__PATH__(self._temp(suffix, prefix, dir))

    def __enter__(self):
        return self.path

    def __exit__(self, exc, value, tb):
        self.delete()

    def __repr__(self):
        return repr(self.path)

    def __str__(self):
        return str(self.path)

    @staticmethod
    def _temp(suffix, prefix, dir):
        pass

    def delete(self):
        pass

    @property
    def path(self):
        return self._path


# noinspection PyShadowingBuiltins
class LazyTempDir(_LazyTempMixin):

    @staticmethod
    def _temp(suffix, prefix, dir):
        return _mkdtemp(suffix, prefix, dir)

    def delete(self):
        if self.path.exists():
            _rmtree(str(self))


# noinspection PyShadowingBuiltins
class LazyTempFile(_LazyTempMixin):

    @staticmethod
    def _temp(suffix, prefix, dir):
        return _mkstemp(suffix, prefix, dir)[1]

    def delete(self):
        if self.path.exists():
            _remove(str(self.path))
