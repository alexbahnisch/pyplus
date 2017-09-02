#!/usr/bin/env python
from re import compile

CAMEL_CASE_SPACE1 = compile(r"([A-Z])([A-Z][a-z]+)")
CAMEL_CASE_SPACE2 = compile(r"([a-z\d])([A-Z])")
INVALID_CHARS = compile(r"\W")
INVALID_LEAD = compile(r"^[^a-zA-Z]+")
REPLACEABLE_WITH_UNDERSCORE = compile(r"[\s/\\,.+-]+")
UNDERSCORES = compile(r"(_)\1+")


def snake_case(string):
    string = REPLACEABLE_WITH_UNDERSCORE.sub(r"_", string)
    string = INVALID_CHARS.sub(r"", string)
    string = UNDERSCORES.sub(r"_", string)
    string = INVALID_LEAD.sub(r"", string)
    string = CAMEL_CASE_SPACE1.sub(r"\1_\2", string)
    string = CAMEL_CASE_SPACE2.sub(r"\1_\2", string)
    return string.lower()
