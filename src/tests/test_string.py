#!/usr/bin/env python
from pyplus.string import alias2keys, camel_case, snake_case, title_case
from pytest import raises

STRINGS = [
    "TestCase", "test_case", "Test Case", "testCase", "_test_case", "test-case", "test+Case", "Test.case",
    "Test, Case", "0%Test_Case", "#1Test_Case"
]

B_STRINGS = [
    b"TestCase", b"test_case", b"Test Case", b"testCase", b"_test_case", b"test-case", b"test+Case", b"Test.case",
    b"Test, Case", b"0%Test_Case", b"#1Test_Case"
]

U_STRINGS = [
    u"TestCase", u"test_case", u"Test Case", u"testCase", u"_test_case", u"test-case", u"test+Case", u"Test.case",
    u"Test, Case", u"0%Test_Case", u"#1Test_Case"
]


def test_alias():
    assert ["key1", "key2", "key3"] == alias2keys("key1.key2.key3")
    assert ["key1", "key2", "key3"] == alias2keys("key1/key2/key3")
    assert ["key1", "key2", "key3"] == alias2keys("key1\key2\key3")
    assert ["key1", "key2", "key3"] == alias2keys("key1>key2>key3")
    assert ["key1", 2, "key3"] == alias2keys("key1[2].key3")
    assert ["key1", 2, 3] == alias2keys("key1>2>3")


def test_alias_bytes():
    assert [b"key1", b"key2", b"key3"] == alias2keys(b"key1.key2.key3")
    assert [b"key1", b"key2", b"key3"] == alias2keys(b"key1/key2/key3")
    assert [b"key1", b"key2", b"key3"] == alias2keys(b"key1\key2\key3")
    assert [b"key1", b"key2", b"key3"] == alias2keys(b"key1>key2>key3")
    assert [b"key1", 2, b"key3"] == alias2keys(b"key1[2].key3")
    assert [b"key1", 2, 3] == alias2keys(b"key1>2>3")


def test_alias_unicode():
    assert [u"key1", u"key2", u"key3"] == alias2keys(u"key1.key2.key3")
    assert [u"key1", u"key2", u"key3"] == alias2keys(u"key1/key2/key3")
    assert [u"key1", u"key2", u"key3"] == alias2keys(u"key1\key2\key3")
    assert [u"key1", u"key2", u"key3"] == alias2keys(u"key1>key2>key3")
    assert [u"key1", 2, u"key3"] == alias2keys(u"key1[2].key3")
    assert [u"key1", 2, 3] == alias2keys(u"key1>2>3")


def test_alias_other():
    assert [] == alias2keys(None)
    assert [0] == alias2keys(0)
    assert [1.5] == alias2keys(1.5)

    with raises(TypeError, message="'bool' object is not a string"):
        alias2keys(True)


def test_camel_case():
    for string in STRINGS:
        assert "TestCase" == camel_case(string)


def test_camel_case_bytes():
    for string in B_STRINGS:
        assert b"TestCase" == camel_case(string)


def test_camel_case_unicode():
    for string in U_STRINGS:
        assert u"TestCase" == camel_case(string)


def test_camel_case_lower():
    for string in STRINGS:
        assert "testCase" == camel_case(string, title=False)


def test_camel_case_lower_bytes():
    for string in B_STRINGS:
        assert b"testCase" == camel_case(string, title=False)


def test_camel_case_lower_unicode():
    for string in U_STRINGS:
        assert u"testCase" == camel_case(string, title=False)


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
