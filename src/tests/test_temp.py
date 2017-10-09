#!/usr/bin/env python
from pyplus.temp import *


def test_lazy_temp_dir():
    lazy_temp_dir = LazyTempDir()
    assert lazy_temp_dir.path.exists()
    lazy_temp_dir.delete()
    assert not lazy_temp_dir.path.exists()


def test_lazy_temp_dir_context():
    with LazyTempDir() as temp_dir:
        assert temp_dir.exists()
    assert not temp_dir.exists()

