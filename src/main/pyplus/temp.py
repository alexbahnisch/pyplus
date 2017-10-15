#!/usr/bin/env python
from os import close as _close, remove as _remove
from shutil import rmtree as _rmtree
from tempfile import mkdtemp as _mkdtemp, mkstemp as _mkstemp

from .path import LazyPath as _LazyPath


# noinspection PyShadowingBuiltins
class _LazyTempMixin:
    __PATH__ = _LazyPath
    __TEMP__ = None

    def __init__(self, path):
        self._path = self.__PATH__(path)

    def __enter__(self):
        return self.path

    def __exit__(self, exc, value, tb):
        self.delete()

    def __repr__(self):
        return repr(self.path)

    def __str__(self):
        return str(self.path)

    def delete(self):
        pass

    @property
    def path(self):
        return self._path


# noinspection PyShadowingBuiltins
class LazyTempDir(_LazyTempMixin):

    def __init__(self, dir=None, prefix=None, suffix=None):
        self.__PATH__.make_dir(dir)
        super().__init__(_mkdtemp(dir=dir, prefix=prefix, suffix=suffix))

    def delete(self):
        if self.path.exists():
            _rmtree(str(self))


# noinspection PyShadowingBuiltins
class LazyTempFile(_LazyTempMixin):

    def __init__(self, dir=None, prefix=None, suffix=None, text=True):
        self.__PATH__.make_dir(dir)
        level, path = _mkstemp(dir=dir, prefix=prefix, suffix=suffix, text=text)
        super().__init__(path)
        self._os_level = level

    def delete(self):
        if self.path.exists():
            _close(self._os_level)
            _remove(str(self.path))
