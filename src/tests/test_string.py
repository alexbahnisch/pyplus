#!/usr/bin/env python
from pyplus.string import camel_case, snake_case, title_case


STRINGS = [
    "TestCase",
    "test_case",
    "Test Case",
    "testCase",
    "_test_case",
    "Test_Case",
    "#1Test_Case"
]

B_STRINGS = [
    b"TestCase",
    b"test_case",
    b"Test Case",
    b"testCase",
    b"_test_case",
    b"Test_Case",
    b"#1Test_Case"
]

U_STRINGS = [
    u"TestCase",
    u"test_case",
    u"Test Case",
    u"testCase",
    u"_test_case",
    u"Test_Case",
    u"#1Test_Case"
]


def test_camel_case():
    for string in STRINGS:
        assert "TestCase" == camel_case(string)


def test_camel_case_bytes():
    for string in B_STRINGS:
        assert b"TestCase" == camel_case(string)


def test_camel_case_unicode():
    for string in U_STRINGS:
        assert u"TestCase" == camel_case(string)


def test_snake_case():
    for string in STRINGS:
        assert "test_case" == snake_case(string)


def test_snake_case_bytes():
    for string in B_STRINGS:
        assert b"test_case" == snake_case(string)


def test_snake_case_unicode():
    for string in U_STRINGS:
        assert u"test_case" == snake_case(string)


def test_title_case():
    for string in STRINGS:
        assert "Test Case" == title_case(string)


def test_title_case_bytes():
    for string in B_STRINGS:
        assert b"Test Case" == title_case(string)


def test_title_case_unicode():
    for string in U_STRINGS:
        assert u"Test Case" == title_case(string)


if __name__ == "__main__":
    test_snake_case()
    test_snake_case_bytes()
    test_snake_case_unicode()
