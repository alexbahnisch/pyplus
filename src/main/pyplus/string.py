#!/usr/bin/env python
from re import compile as _compile

from .decorators import parser as _parser
from .parse import parse as _parse


ALIAS_SPLIT = _compile(u"[\[./\\\]]")
CAMEL_CASE_SPACE1 = _compile(u"([A-Z])([A-Z][a-z]+)")
CAMEL_CASE_SPACE2 = _compile(u"([a-z\d])([A-Z])")
CAPITALS = _compile(u"([A-Z])([A-Z])")
CAPITAL_LOWER = _compile(u"([A-Z])([a-z])")
INVALID_CHARS = _compile(u"\W")
INVALID_LEAD = _compile(u"^[^a-zA-Z]+")
REPLACEABLE_WITH_UNDERSCORE = _compile(u"[\s/,.+-]+")
SPACE = _compile(u" ")
UNDERSCORE = _compile(u"_")
UNDERSCORES = _compile(u"(_)\1+")


@_parser
def alias2keys(alias):
    return map(lambda string: _parse(string, False), filter(None, ALIAS_SPLIT.split(alias)))


def _base_case(string):
    string = REPLACEABLE_WITH_UNDERSCORE.sub(r"_", string)
    string = INVALID_CHARS.sub(r"", string)
    string = CAMEL_CASE_SPACE1.sub(r"\1_\2", string)
    return CAMEL_CASE_SPACE2.sub(r"\1_\2", string)


@_parser
def camel_case(string):
    string = _base_case(string)
    string = UNDERSCORE.sub(r" ", string)
    string = CAPITALS.sub(r"\1 \2", string).title()
    string = SPACE.sub(r"", string)
    return INVALID_LEAD.sub(r"", string)


@_parser
def snake_case(string):
    string = _base_case(string)
    string = UNDERSCORES.sub(r"_", string)
    return INVALID_LEAD.sub(r"", string).lower()


@_parser
def title_case(string):
    string = _base_case(string)
    string = UNDERSCORE.sub(r" ", string)
    string = CAPITALS.sub(r"\1 \2", string).title()
    string = SPACE.sub(r"", string)
    string = CAPITAL_LOWER.sub(r" \1\2", string)
    return INVALID_LEAD.sub(r"", string)
