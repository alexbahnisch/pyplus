#!/usr/bin/env python
from collections import OrderedDict

if __name__ == "__main__":
    a = {"a": 1, "b": 2}
    b = OrderedDict({"b": 2, "a": 1})
    assert a.keys() == b.keys()
    assert a.values() == b.values()
