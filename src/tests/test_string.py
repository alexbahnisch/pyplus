#!/usr/bin/env python
from pyplus.string import snake_case


STRINGS = [
    "CamelCase2SnakeCase",
    "camelCase2SnakeCase"
]

B_STRINGS = [
    b"CamelCase2SnakeCase",
    b"camelCase2SnakeCase"
]

U_STRINGS = [
    u"CamelCase2SnakeCase",
    u"camelCase2SnakeCase"
]


def test_snake_case():
    for string in STRINGS:
        assert "camel_case2_snake_case" == snake_case(string)


def test_snake_case_bytes():
    for string in B_STRINGS:
        assert b"camel_case2_snake_case" == snake_case(string)


def test_snake_case_unicode():
    for string in U_STRINGS:
        assert u"camel_case2_snake_case" == snake_case(string)


if __name__ == "__main__":
    test_snake_case()
    test_snake_case_bytes()
    test_snake_case_unicode()
