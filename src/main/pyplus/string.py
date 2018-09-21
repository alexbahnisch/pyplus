"""
A collection of string helper functions.
"""
from re import compile as _compile

from .decorators import parser as _parser, spliter as _spliter
from .parse import parse as _parse

ALIAS_SPLIT = _compile(r"[\[./\\\]>]")
CAMEL_CASE_SPACE1 = _compile(r"([A-Z])([A-Z][a-z]+)")
CAMEL_CASE_SPACE2 = _compile(r"([a-z\d])([A-Z])")
CAPITALS = _compile(r"([A-Z])([A-Z])")
CAPITAL_LOWER = _compile(r"([A-Z])([a-z])")
INVALID_CHARS = _compile(r"\W")
INVALID_LEAD = _compile(r"^[^a-zA-Z]+")
REPLACEABLE_WITH_UNDERSCORE = _compile(r"[\s/,.+-]+")
SPACE = _compile(r" ")
UNDERSCORE = _compile(r"_")
UNDERSCORES = _compile(r"(_)\1+")


def _base_case(string):
    string = REPLACEABLE_WITH_UNDERSCORE.sub(r"_", string)
    string = INVALID_CHARS.sub(r"", string)
    string = CAMEL_CASE_SPACE1.sub(r"\1_\2", string)
    return CAMEL_CASE_SPACE2.sub(r"\1_\2", string)


@_spliter
def alias2keys(alias):
    """
    Splits an alias into a list of keys.
    @param alias: {string} An alias (e.g. 'key0.key1.key2').
    @return: {list} Returns a list of string keys.
    """
    return [_parse(key, errors=False) for key in filter(None, ALIAS_SPLIT.split(alias))]


@_parser
def camel_case(string, title=True):
    """
    @param string:
    @param title:
    @return:
    """
    string = _base_case(string)
    string = UNDERSCORE.sub(r" ", string)
    string = CAPITALS.sub(r"\1 \2", string).title()
    string = SPACE.sub(r"", string)
    string = INVALID_LEAD.sub(r"", string)
    if not title:
        string = string[0].lower() + string[1:]
    return string


def extract_between(string, start=None, end=None):
    if start is None:
        start_index = 0
    else:
        start_index = string.find(start)
        start_index = start_index + len(start) if start_index >= 0 else 0

    if end is None:
        end_index = len(string)
        end_start_index = end_index
    else:
        end_index = string.find(end)
        if end_index >= 0:
            end_start_index = end_index + len(end)
        else:
            end_index = 0
            end_start_index = 0

    return string[start_index:end_index], string[end_start_index:len(string)]


@_parser
def kebab_case(string):
    string = _base_case(string)
    string = UNDERSCORES.sub(r"_", string)
    string = UNDERSCORE.sub(r"-", string)
    return INVALID_LEAD.sub(r"", string).lower()


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
