#!/usr/bin/env python
from pyplus.json import json


class Object(object):

    def __init__(self, *args):
        self._args = list(args)

    def __len__(self):
        return len(self._args)

    def __iter__(self):
        return iter(self._args)

    def __getitem__(self, index):
        return self._args[index]


if __name__ == "__main__":
    a = json.from_path("../resources/json/json.json")
    pass
