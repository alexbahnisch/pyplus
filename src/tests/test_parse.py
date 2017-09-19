#!/usr/bin/env python
from pytest import raises
from pyplus.parse import *


def fun(arg):
    return arg


def test_create_parse():
    par = create_parser(False)
    assert "string" == par("string")
    assert b"string" == par(b"string")
    assert u"string" == par(u"string")
    assert parse is create_parser(True)
    assert fun is create_parser(fun)


def test_lazy_parse():
    assert 1 == lazy_parse("1")
    assert -1.5 == lazy_parse("-3 / 2")
    assert False is lazy_parse("False")
    assert None is lazy_parse("None")
    assert True is lazy_parse("True")
    assert {u"key": b"value"} == lazy_parse("{u'key': b'value'}")
    assert [1, 1.5] == lazy_parse("[1, 1.5]")
    assert {True, False, None} == lazy_parse("{True, False,  None}")
    assert ("1", "2") == lazy_parse("('1', '2')")


def test_lazy_parse_bytes():
    assert 1 == lazy_parse(b"1")
    assert -1.5 == lazy_parse(b"-3 / 2")
    assert False is lazy_parse(b"False")
    assert None is lazy_parse(b"None")
    assert True is lazy_parse(b"True")
    assert {u"key": b"value"} == lazy_parse(b"{u'key': b'value'}")
    assert [1, 1.5] == lazy_parse(b"[1, 1.5]")
    assert {True, False, None} == lazy_parse(b"{True, False, None}")
    assert ("1", "2") == lazy_parse(b"('1', '2')")


def test_lazy_parse_unicode():
    assert 1 == lazy_parse(u"1")
    assert -1.5 == lazy_parse(u"-3 / 2")
    assert False is lazy_parse(u"False")
    assert None is lazy_parse(u"None")
    assert True is lazy_parse(u"True")
    assert {u"key": b"value"} == lazy_parse(u"{u'key': b'value'}")
    assert [1, 1.5] == lazy_parse(u"[1, 1.5]")
    assert {True, False, None} == lazy_parse(u"{True, False, None}")
    assert ("1", "2") == lazy_parse(u"('1', '2')")


def test_lazy_parse_exception():
    with raises(ValueError, message="could not parse string: 'string'"):
        lazy_parse("string", errors=True)
    assert lazy_parse("string") == "string"

    with raises(ValueError, message="could not parse string: 'string + 5'"):
        lazy_parse("string + 5", errors=True)
    assert lazy_parse("string + 5") == "string + 5"

    with raises(ValueError, message="could not parse string: '[1, 2)'"):
        lazy_parse("[1, 2)", errors=True)
    assert lazy_parse("[1, 2)") == "[1, 2)"

    with raises(ValueError, message="could not parse string: 'a = 5'"):
        lazy_parse("a = 5", errors=True)
    assert lazy_parse("a = 5") == "a = 5"


def test_lazy_parse_exception_bytes():
    with raises(ValueError, message="could not parse string: 'string'"):
        lazy_parse(b"string", errors=True)
    assert lazy_parse(b"string") == b"string"

    with raises(ValueError, message="could not parse string: 'string + 5'"):
        lazy_parse(b"string + 5", errors=True)
    assert lazy_parse(b"string + 5") == b"string + 5"

    with raises(ValueError, message="could not parse string: '[1, 2)'"):
        lazy_parse(b"[1, 2)", errors=True)
    assert lazy_parse(b"[1, 2)") == b"[1, 2)"

    with raises(ValueError, message="could not parse string: 'a = 5'"):
        lazy_parse(b"a = 5", errors=True)
    assert lazy_parse(b"a = 5") == b"a = 5"


def test_lazy_parse_exception_unicode():
    with raises(ValueError, message="could not parse string: 'string'"):
        lazy_parse(u"string", errors=True)
    assert lazy_parse(u"string") == "string"

    with raises(ValueError, message="could not parse string: 'string + 5'"):
        lazy_parse(u"string + 5", errors=True)
    assert lazy_parse(u"string + 5") == u"string + 5"

    with raises(ValueError, message="could not parse string: '[1, 2)'"):
        lazy_parse(u"[1, 2)", errors=True)
    assert lazy_parse(u"[1, 2)") == u"[1, 2)"

    with raises(ValueError, message="could not parse string: 'a = 5'"):
        lazy_parse(u"a = 5", errors=True)
    assert lazy_parse(u"a = 5") == u"a = 5"


def test_parse():
    assert 1 == parse("1")
    assert -1.5 == parse("-3 / 2")
    assert False is parse("false")
    assert None is parse("null")
    assert True is parse("true")
    assert {u"key": b"value"} == parse("{u'key': b'value'}")
    assert [1, 1.5] == parse("[1, 1.5]")
    assert {True, False, None} == parse("{True, False, None}")
    assert ("1", "2") == parse("('1', '2')")
    assert "string" == parse("string")


def test_parse_bytes():
    assert 1 == parse(b"1")
    assert -1.5 == parse(b"-3 / 2")
    assert False is parse(b"false")
    assert None is parse(b"null")
    assert True is parse(b"true")
    assert {u"key": b"value"} == parse(b"{u'key': b'value'}")
    assert [1, 1.5] == parse(b"[1, 1.5]")
    assert {True, False, None} == parse(b"{True, False, None}")
    assert ("1", "2") == parse(b"('1', '2')")
    assert b"string" == parse(b"string")


def test_parse_unicode():
    assert 1 == parse(u"1")
    assert -1.5 == parse(u"-3 / 2")
    assert False is parse(u"false")
    assert None is parse(u"null")
    assert True is parse(u"true")
    assert {u"key": b"value"} == parse(u"{u'key': b'value'}")
    assert [1, 1.5] == parse(u"[1, 1.5]")
    assert {True, False, None} == parse(u"{True, False, None}")
    assert ("1", "2") == parse(u"('1', '2')")
    assert u"string" == parse(u"string")


def test_parse_exception():
    with raises(ValueError, message="could not parse string: 'string'"):
        parse("string", errors=True)
    assert parse("string") == "string"

    with raises(ValueError, message="could not parse string: 'x'"):
        parse("x", errors=True)
    assert parse("x") == "x"


def test_parse_exception_bytes():
    with raises(ValueError, message="could not parse string: 'string'"):
        parse(b"string", errors=True)
    assert parse(b"string") == b"string"

    with raises(ValueError, message="could not parse string: 'x'"):
        parse(b"x", errors=True)
    assert parse(b"x") == b"x"


def test_parse_exception_unicode():
    with raises(ValueError, message="could not parse string: 'string'"):
        parse(u"string", errors=True)
    assert parse(u"string") == u"string"

    with raises(ValueError, message="could not parse string: 'x'"):
        parse(u"x", errors=True)
    assert parse(u"x") == u"x"


def test_parser_bool():
    assert False is parse_bool("False")
    assert False is parse_bool("false")
    assert False is parse_bool("FALSE")
    assert True is parse_bool("True")
    assert True is parse_bool("true")
    assert True is parse_bool("TRUE")


def test_parser_bool_bytes():
    assert True is parse_bool(b"True")
    assert True is parse_bool(b"true")
    assert True is parse_bool(b"TRUE")
    assert False is parse_bool(b"False")
    assert False is parse_bool(b"false")
    assert False is parse_bool(b"FALSE")


def test_parser_bool_unicode():
    assert True is parse_bool(u"True")
    assert True is parse_bool(u"true")
    assert True is parse_bool(u"TRUE")
    assert False is parse_bool(u"False")
    assert False is parse_bool(u"false")
    assert False is parse_bool(u"FALSE")


def test_parse_bool_exception():
    with raises(ValueError, message="could not convert string to bool: '0'"):
        parse_bool("0", errors=True)
    assert parse_bool("0") == "0"

    with raises(ValueError, message="could not convert string to bool: 'T'"):
        parse_bool("T", errors=True)
    assert parse_bool("T") == "T"

    with raises(ValueError, message="could not convert string to bool: 'None'"):
        parse_bool("None", errors=True)
    assert parse_bool("None") == "None"


def test_parse_bool_exception_bytes():
    with raises(ValueError, message="could not convert string to bool: '0'"):
        parse_bool(b"0", errors=True)
    assert parse_bool(b"0") == b"0"

    with raises(ValueError, message="could not convert string to bool: 'T'"):
        parse_bool(b"T", errors=True)
    assert parse_bool(b"T") == b"T"

    with raises(ValueError, message="could not convert string to bool: 'None'"):
        parse_bool(b"None", errors=True)
    assert parse_bool(b"None") == b"None"


def test_parse_bool_exception_unicode():
    with raises(ValueError, message="could not convert string to bool: '0'"):
        parse_bool(u"0", errors=True)
    assert parse_bool(u"0") == u"0"

    with raises(ValueError, message="could not convert string to bool: 'T'"):
        parse_bool(u"T", errors=True)
    assert parse_bool(u"T") == u"T"

    with raises(ValueError, message="could not convert string to bool: 'None'"):
        parse_bool(u"None", errors=True)
    assert parse_bool(u"None") == u"None"


def test_parse_none():
    assert None is parse_none("")
    assert None is parse_none("None")
    assert None is parse_none("null")
    assert None is parse_none("undefined")


def test_parse_none_bytes():
    assert None is parse_none(b"")
    assert None is parse_none(b"None")
    assert None is parse_none(b"null")
    assert None is parse_none(b"undefined")


def test_parse_none_unicode():
    assert None is parse_none(u"")
    assert None is parse_none(u"None")
    assert None is parse_none(u"null")
    assert None is parse_none(u"undefined")


def test_parse_none_exception():
    with raises(ValueError, message="could not convert string to None: '0'"):
        parse_none("0", errors=True)
    assert parse_none("0") == "0"

    with raises(ValueError, message="could not convert string to None: 'False'"):
        parse_none("False", errors=True)
    assert parse_none("False") == "False"

    with raises(ValueError, message="could not convert string to None: 'n'"):
        parse_none("n", errors=True)
    assert parse_none("n") == "n"


def test_parse_none_exception_bytes():
    with raises(ValueError, message="could not convert string to None: '0'"):
        parse_none(b"0", errors=True)
    assert parse_none(b"0") == b"0"

    with raises(ValueError, message="could not convert string to None: 'False'"):
        parse_none(b"False", errors=True)
    assert parse_none(b"False") == b"False"

    with raises(ValueError, message="could not convert string to None: 'n'"):
        parse_none(b"n", errors=True)
    assert parse_none(b"n") == b"n"


def test_parse_none_exception_unicode():
    with raises(ValueError, message="could not convert string to None: '0'"):
        parse_none(u"0", errors=True)
    assert parse_none(u"0") == u"0"

    with raises(ValueError, message="could not convert string to None: 'False'"):
        parse_none(u"False", errors=True)
    assert parse_none(u"False") == u"False"

    with raises(ValueError, message="could not convert string to None: 'n'"):
        parse_none(u"n", errors=True)
    assert parse_none(u"n") == u"n"
