#!/usr/bin/env python
from pyplus.common import iswindows
from pyplus.temp import *


def test_lazy_temp_dir():
    lazy_temp_dir = LazyTempDir()
    assert lazy_temp_dir.path.exists()
    assert str(lazy_temp_dir.path) == str(lazy_temp_dir)
    assert repr(lazy_temp_dir.path) == repr(lazy_temp_dir)
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

    if not iswindows():
        # TODO - work out permanent fix for windows
        lazy_temp_file.delete()
        assert not lazy_temp_file.path.exists()
