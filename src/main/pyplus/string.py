"""
A collection of string helper functions.
"""
from re import compile as _compile

from .common import isstring as _isstring
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
    @param alias: {string} An alias/path (e.g. 'key0.key1.key2').
    @return: {list} Returns a list of string keys.
    """
    return [_parse(key, errors=False) for key in filter(None, ALIAS_SPLIT.split(alias))]


@_parser
def camel_case(string, title=True):
    """
    Convert string to 'camelCase'.
    @param string: {string} The string to convert.
    @param title: {bool} Return 'PascalCase' instead of camelcase
    @return: {string} Returns the 'camelCased' string.
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
    """
    Extracts text between the first instances of 'start' and 'end', returns the remaining string and the extracted text
    @param string: {string} String to extract text between.
    @param start: {string} Extract text after this value, if 'None' extract all text from and including the start of the string.
    @param end: {string} Extract text before this value, if 'None' extract all text up to and including the end of the string.
    @return: {string} Extracted string.
    @return: {string} Remaining text from the input 'string'.
    """
    if not all([_isstring(string), _isstring(start) or start is None, _isstring(end) or end is None]):
        raise TypeError("'string' args must be a string and 'start' and 'end' kwargs be strings or None")

    if start is None:
        start_index = 0
    else:
        start_index = string.find(start)
        start_index = start_index + len(start) if start_index >= 0 else 0

    if end is None:
        end_index = len(string)
    else:
        end_index = string.find(end)
        if end_index < 0:
            end_index = 0

    value = string[start_index:end_index]
    return value, string.replace((start or "") + value + (end or ""), "")


@_parser
def kebab_case(string):
    """
    Convert string to 'kebab-case'.
    @param string: {string} The string to convert.
    @return: {string} Returns the 'kebab-case' string.
    """
    string = _base_case(string)
    string = UNDERSCORES.sub(r"_", string)
    string = UNDERSCORE.sub(r"-", string)
    return INVALID_LEAD.sub(r"", string).lower()


@_parser
def snake_case(string):
    """
    Convert string to 'snake_case'.
    @param string: {string} The string to convert.
    @return: {string} Returns the 'snake_case' string.
    """
    string = _base_case(string)
    string = UNDERSCORES.sub(r"_", string)
    return INVALID_LEAD.sub(r"", string).lower()


@_parser
def title_case(string):
    """
    Convert string to 'Title Case'.
    @param string: {string} The string to convert.
    @return: {string} Returns the 'Title Case' string.
    """
    string = _base_case(string)
    string = UNDERSCORE.sub(r" ", string)
    string = CAPITALS.sub(r"\1 \2", string).title()
    string = SPACE.sub(r"", string)
    string = CAPITAL_LOWER.sub(r" \1\2", string)
    return INVALID_LEAD.sub(r"", string)
