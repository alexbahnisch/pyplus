#!/usr/bin/env python3
from pyplus.temp import *


def test_lazy_temp_dir():
    lazy_temp_dir = LazyTempDir()
    assert lazy_temp_dir.path.exists()
    assert str(lazy_temp_dir.path) == str(lazy_temp_dir)
    assert repr(lazy_temp_dir.path) == repr(lazy_temp_dir)
    lazy_temp_dir.delete()
    assert not lazy_temp_dir.path.exists()


def test_lazy_temp_dir_mkdir():
    with LazyTempDir() as lazy_dir:
        lazy_temp_dir = LazyTempDir(dir=str(lazy_dir.joinpath("./test")))
        lazy_temp_dir.delete()

    assert not lazy_temp_dir.path.exists()


def test_lazy_temp_dir_context():
    with LazyTempDir() as temp_dir:
        assert temp_dir.exists()
    assert not temp_dir.exists()


def test_lazy_temp_file():
    lazy_temp_file = LazyTempFile()
    assert lazy_temp_file.path.exists()
    assert str(lazy_temp_file.path) == str(lazy_temp_file)
    assert repr(lazy_temp_file.path) == repr(lazy_temp_file)

    lazy_temp_file.delete()
    assert not lazy_temp_file.path.exists()


def test_lazy_temp_file_mkdir():
    with LazyTempDir() as lazy_dir:
        lazy_temp_dir = LazyTempFile(dir=str(lazy_dir.joinpath("./test")))
        lazy_temp_dir.delete()

    assert not lazy_temp_dir.path.exists()
