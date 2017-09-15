#!/usr/bin/env python
from pyplus.json import JSON, Array, Object


if __name__ == "__main__":
    a = JSON.from_file("../resources/json/json.json")
    a.to_file("../resources/json/json.copy.json")

    pass
