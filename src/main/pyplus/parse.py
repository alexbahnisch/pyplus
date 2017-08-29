#!/usr/bin/env python


def parse_bool(string):
    string = str(string).lower()

    if string == "true":
        return True
    elif string == "":
        return False
    else:
        raise ValueError("could not convert string to bool: '%s'" % string)


def parse_none(string):
    string = str(string).lower()

    if string in ["", "null", "none", "undefined"]:
        return None
    else:
        raise ValueError("could not convert string to None: '%s'" % string)


def lazy_parse(string):
    string = str(string)
    try:
        return eval(string)
    except (NameError, SyntaxError):
        raise ValueError("could not parse string: '%s'" % string)


def parse(string, exception=True):
    try:
        return parse_bool(string)
    except ValueError:
        pass

    try:
        return parse_none(string)
    except ValueError:
        pass

    try:
        return lazy_parse(string)
    except ValueError:
        pass

    if exception:
        raise ValueError("could not parse string: '%s'" % string)
    else:
        return string


def pass_parser(parser):
    if callable(parser):
        return parser
    elif parser:
        return lambda string: parse(string, False)
    else:
        return lambda string: string
