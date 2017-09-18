from .decorators import parser as _parser


def __parse_bool(string):
    string = str(string).lower()

    if string == "true":
        return True
    elif string == "false":
        return False
    else:
        raise ValueError("could not convert string to bool: '%s'" % string)


def __parse_none(string):
    string = str(string).lower()

    if string in ["", "null", "none", "undefined"]:
        return None
    else:
        raise ValueError("could not convert string to None: '%s'" % string)


def __lazy_parse(string):
    if "string" in string:
        raise ValueError("could not parse string: '%s'" % string)
    else:
        try:
            return eval(string)
        except (NameError, SyntaxError):
            raise ValueError("could not parse string: '%s'" % string)


@_parser
def parse(string, errors=False):
    try:
        return __parse_bool(string)
    except ValueError:
        pass

    try:
        return __parse_none(string)
    except ValueError:
        pass

    try:
        return __lazy_parse(string)
    except ValueError:
        pass

    if bool(errors):
        raise ValueError("could not parse string: '%s'" % string)
    else:
        return string


def create_parser(arg):
    if callable(arg):
        return arg
    elif bool(arg):
        return parse
    else:
        return lambda string: string


parse_bool = _parser(__parse_bool)
parse_none = _parser(__parse_none)
lazy_parse = _parser(__lazy_parse)
