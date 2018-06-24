from os import close as _close, remove as _remove
from pathlib import Path as _Path, PosixPath as _PosixPath, WindowsPath as _WindowsPath
from shutil import rmtree as _rmtree
from tempfile import mkdtemp as _mkdtemp, mkstemp as _mkstemp

from .common import ispathlike as _ispathlike, iswindows as _iswindows


# noinspection PyAbstractClass,PyArgumentList,PyTypeChecker,PyShadowingBuiltins
class LazyPath(_Path):
    __POSIX__ = _PosixPath
    __WINDOWS__ = _WindowsPath

    def __new__(cls, *args, **kwargs):
        if issubclass(cls, LazyPath):
            cls = cls.__WINDOWS__ if _iswindows() else cls.__POSIX__
            self = cls._from_parts(args, init=False)
            self._init()
            return self
        else:
            raise NotImplementedError("cannot instantiate %r on your system" % (cls.__name__,))

    @classmethod
    def make_dir(cls, dir):
        if _ispathlike(dir):
            dir = cls(dir)
            dir.mkdir()

    @classmethod
    def new_dir(cls, path=None, dir=None, prefix=None, suffix=None):
        if path is None:
            cls.make_dir(dir)
            lazy_dir = cls(_mkdtemp(dir=dir, prefix=prefix, suffix=suffix))
        elif _ispathlike(path):
            lazy_dir = cls(path)
            lazy_dir.mkdir()
        else:
            raise TypeError("'path 'argument should be a None, path or str object, not '%s'" % type(path).__name__)

        return lazy_dir.resolve()

    @classmethod
    def new_file(cls, path=None, dir=None, prefix=None, suffix=None, text=True):
        if path is None:
            cls.make_dir(dir)
            level, path = _mkstemp(dir=dir, prefix=prefix, suffix=suffix, text=text)
            lazy_file = cls(path)
            lazy_file.resolve()
            lazy_file._os_level = level
        elif _ispathlike(path):
            lazy_file = cls(path)
            lazy_file.touch()
            lazy_file.resolve()
        else:
            raise TypeError("'path 'argument should be a None, path or str object, not '%s'" % type(path).__name__)

        return lazy_file

    def _init(self, template=None):
        self._os_level = None
        super()._init(template=template)

    def delete(self, recursive=False):
        if self.is_file():
            if isinstance(self._os_level, int):
                _close(self._os_level)
            _remove(str(self))
        elif self.is_dir():
            if recursive:
                _rmtree(str(self))
            else:
                self.rmdir()

    def mkdir(self, mode=0o777, parents=True, exist_ok=True):
        super().mkdir(mode, parents, exist_ok)

    def open(self, mode="r", buffering=-1, encoding=None, errors=None, newline=None):
        self.touch()
        return super().open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)

    def read(self, mode="r", buffering=-1, encoding=None, errors=None, newline=None):
        return self.open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)

    def touch(self, mode=0o777, parents=True, exist_ok=True):
        self.parent.mkdir(mode, parents, exist_ok)
        super().touch(mode, exist_ok)

    def write(self, mode="w", buffering=-1, encoding=None, errors=None, newline=None):
        return self.open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)


# noinspection PyAbstractClass
class LazyPosixPath(LazyPath, _PosixPath):
    pass


# noinspection PyAbstractClass
class LazyWindowsPath(LazyPath, _WindowsPath):
    pass


LazyPath.__POSIX__ = LazyPosixPath
LazyPath.__WINDOWS__ = LazyWindowsPath
