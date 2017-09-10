#!/usr/bin/env python
from re import compile as _compile

from .decorators import parser as _parser
from .parse import parse as _parse


ALIAS_SPLIT = "[\[./\\\]]"
CAMEL_CASE_SPACE1 = _compile(u"([A-Z])([A-Z][a-z]+)")
CAMEL_CASE_SPACE2 = _compile(u"([a-z\d])([A-Z])")
INVALID_CHARS = _compile(u"\W")
INVALID_LEAD = _compile(u"^[^a-zA-Z]+")
REPLACEABLE_WITH_UNDERSCORE = _compile(u"[\s/,.+-]+")
UNDERSCORES = _compile(u"(_)\1+")


@_parser
def alias2keys(alias):
    return map(lambda string: _parse(string, False), filter(None, ALIAS_SPLIT.split(alias)))


@_parser
def snake_case(string):
    string = REPLACEABLE_WITH_UNDERSCORE.sub("_", string)
    string = INVALID_CHARS.sub("", string)
    string = UNDERSCORES.sub("_", string)
    string = INVALID_LEAD.sub("", string)
    string = CAMEL_CASE_SPACE1.sub(r"\1_\2", string)
    string = CAMEL_CASE_SPACE2.sub(r"\1_\2", string)
    return string.lower()
