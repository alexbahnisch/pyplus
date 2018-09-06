#!/usr/bin/env python3
from pyplus.path import LazyPath
from pyplus.temp import LazyTempDir
from pytest import raises


def test_lazy_path_dir():
    with LazyTempDir() as temp_dir:
        lazy_dir = temp_dir.joinpath("./test/test")
        assert not lazy_dir.exists()
        lazy_dir.mkdir()
        assert lazy_dir.exists()
        assert lazy_dir.is_dir()
        lazy_dir.delete()
        assert not lazy_dir.exists()


def test_lazy_path_file():
    with LazyTempDir() as temp_dir:
        lazy_file = temp_dir.joinpath("./test/test.txt")
        assert not lazy_file.exists()
        lazy_file.touch()
        assert lazy_file.exists()
        assert lazy_file.is_file()
        lazy_file.delete()
        assert not lazy_file.exists()


def test_lazy_path_new_dir():
    with LazyTempDir() as temp_dir:
        lazy_dir = LazyPath.new_dir(temp_dir.joinpath("./test/test"))
        assert lazy_dir.exists()
        assert lazy_dir.is_dir()
        lazy_dir.delete()
        assert not lazy_dir.exists()

        lazy_dir = LazyPath.new_dir(dir=str(temp_dir.joinpath("./test/test")))
        assert lazy_dir.exists()
        assert lazy_dir.is_dir()
        lazy_dir.delete()
        assert not lazy_dir.exists()

    lazy_dir = LazyPath.new_dir()
    assert lazy_dir.exists()
    assert lazy_dir.is_dir()
    lazy_dir.delete()
    assert not lazy_dir.exists()


def test_lazy_path_new_file():
    with LazyTempDir() as temp_dir:
        lazy_file = LazyPath.new_file(temp_dir.joinpath("./test/test.txt"))
        assert lazy_file.exists()
        assert lazy_file.is_file()
        lazy_file.delete()
        assert not lazy_file.exists()

        lazy_file = LazyPath.new_file(dir=str(temp_dir.joinpath("./test/test")))
        assert lazy_file.exists()
        assert lazy_file.is_file()
        lazy_file.delete()
        assert not lazy_file.exists()

    lazy_file = LazyPath.new_file()
    assert lazy_file.exists()
    assert lazy_file.is_file()

    lazy_file.delete()
    assert not lazy_file.exists()


# noinspection PyTypeChecker
def test_lazy_path_exception():
    with LazyTempDir() as temp_dir:
        lazy_dir = temp_dir.joinpath("./test")
        lazy_file = temp_dir.joinpath("./test/test.txt")
        lazy_file.touch()

        with raises(OSError):
            lazy_dir.delete()

        with raises(NotImplementedError, message="cannot instantiate object on your system"):
            LazyPath.__new__(object)

        with raises(TypeError, message="'path 'argument should be a None, path or str object, not 'object'"):
            LazyPath.new_dir(object())

        with raises(TypeError, message="'path 'argument should be a None, path or str object, not 'object'"):
            LazyPath.new_file(object())

        lazy_dir.delete(recursive=True)
