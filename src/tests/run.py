#!/usr/bin/env python
from collections import OrderedDict


def fun(**kwargs):
    print(kwargs)


if __name__ == "__main__":
    a = {"1": 1, "2": 2}
    fun(**a)
