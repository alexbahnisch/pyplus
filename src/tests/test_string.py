#!/usr/bin/env python
from collectivex.string import snake_case

STRINGS = ["CamelCase2SnakeCase"]


def test_snake_case():
    for string in STRINGS:
        assert "camel_case2_snake_case" == snake_case(string)


if __name__ == "__main__":
    test_snake_case()
