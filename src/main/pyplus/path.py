from os import name as _name, remove as _remove
from pathlib import Path as _Path, PosixPath as _PosixPath, WindowsPath as _WindowsPath
from shutil import rmtree as _rmtree
from tempfile import mkdtemp as _mkdtemp


# noinspection PyAbstractClass,PyTypeChecker
class LazyPath(_Path):
    __POSIX__ = _PosixPath
    __WINDOWS__ = _WindowsPath

    def __new__(cls, *args, **kwargs):
        if issubclass(cls, LazyPath):
            cls = cls.__WINDOWS__ if _name == "nt" else cls.__POSIX__
            self = cls._from_parts(args, init=False)
            self._init()
            return self
        else:
            raise NotImplementedError("cannot instantiate %r on your system" % (cls.__name__,))

    def delete(self, recursive=False, errors=False):
        try:
            if self.is_file():
                _remove(str(self))
            elif self.is_dir():
                if bool(recursive):
                    _rmtree(str(self))
                else:
                    self.rmdir()

        except Exception as error:
            if bool(errors):
                raise error

    def read(self, mode="r", buffering=-1, encoding=None, errors=None, newline=None):
        return self.open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)

    def write(self, mode="w", buffering=-1, encoding=None, errors=None, newline=None):
        if not self.parent.exists():
            self.parent.mkdir(parents=True, exist_ok=True)

        if not self.exists():
            self.touch()

        return self.open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)


# noinspection PyAbstractClass
class LazyPosixPath(LazyPath, _PosixPath):
    pass


# noinspection PyAbstractClass
class LazyWindowsPath(LazyPath, _WindowsPath):
    pass


LazyPath.__POSIX__ = LazyPosixPath
LazyPath.__WINDOWS__ = LazyWindowsPath


# noinspection PyShadowingBuiltins
class LazyTempDir:
    __PATH__ = LazyPath

    def __init__(self, suffix=None, prefix=None, dir=None):
        self.__path = self.__PATH__(_mkdtemp(suffix, prefix, dir))

    def __enter__(self):
        return self.path

    def __exit__(self, exc, value, tb):
        self.delete()

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.name

    def delete(self):
        if self.path.exists():
            _rmtree(self.name)

    @property
    def name(self):
        return str(self.__path)

    @property
    def path(self):
        return self.__path
