#!/usr/bin/env python
from pyplus.path import LazyPath, LazyTempDir
from pytest import raises


# noinspection PyTypeChecker
def test_lazy_path():
    with raises(NotImplementedError, message="cannot instantiate object on your system"):
        LazyPath.__new__(object)

    with LazyTempDir() as temp_dir:
        temp_file = LazyPath(temp_dir).joinpath("./temp/temp.txt")
        temp_folder = LazyPath(temp_dir).joinpath("./temp")

        with temp_file.write():
            pass

        temp_folder.delete()

        with raises(OSError):
            temp_folder.delete(errors=True)

        assert temp_dir.exists()
        assert temp_file.exists()
        assert temp_folder.exists()

        temp_folder.delete(recursive=True)

        assert not temp_file.exists()
        assert not temp_folder.exists()

    assert not temp_dir.exists()


def test_lazy_temp_dir():
    lazy_temp_dir = LazyTempDir()
    assert lazy_temp_dir.path.exists()
    lazy_temp_dir.delete()
    assert not lazy_temp_dir.path.exists()


def test_lazy_temp_dir_context():
    with LazyTempDir() as temp_dir:
        assert temp_dir.exists()
    assert not temp_dir.exists()


def test_lazy_temp_dir_name():
    lazy_temp_dir = LazyTempDir("suffix", "prefix")
    with lazy_temp_dir:
        assert "LazyTempDir" in repr(lazy_temp_dir)
        assert "suffix" in repr(lazy_temp_dir)
        assert "prefix" in repr(lazy_temp_dir)
        assert "suffix" in str(lazy_temp_dir)
        assert "prefix" in str(lazy_temp_dir)
