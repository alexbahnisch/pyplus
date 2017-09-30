from .decorators import parser as _parser


def __parse_bool(string, errors=False):
    lower_string = str(string).lower()

    if lower_string == "true":
        return True
    elif lower_string == "false":
        return False
    else:
        if bool(errors):
            raise ValueError("could not convert string to bool: '%s'" % string)
        else:
            return string


parse_bool = _parser(__parse_bool)


def __parse_none(string, errors=False):
    lower_string = str(string).lower()

    if lower_string in ["", "#n/a", "null", "none", "undefined"]:
        return None
    else:
        if bool(errors):
            raise ValueError("could not convert string to None: '%s'" % string)
        else:
            return string


parse_none = _parser(__parse_none)


def __lazy_parse(string, errors=False):
    if "string" in string:
        if bool(errors):
            raise ValueError("could not parse string: '%s'" % string)
        else:
            return string
    else:
        try:
            return eval(string)
        except (NameError, SyntaxError):
            if bool(errors):
                raise ValueError("could not parse string: '%s'" % string)
            else:
                return string


lazy_parse = _parser(__lazy_parse)


@_parser
def parse(string, errors=False):
    try:
        return __parse_bool(string, errors=True)
    except ValueError:
        pass

    try:
        return __parse_none(string, errors=True)
    except ValueError:
        pass

    try:
        return __lazy_parse(string, errors=True)
    except ValueError:
        pass

    if bool(errors):
        raise ValueError("could not parse string: '%s'" % string)
    else:
        return string


def _create_parser(arg, default_parser):
    if callable(arg):
        return arg
    elif bool(arg):
        return default_parser
    else:
        return lambda string: string


def create_lazy_parser(arg):
    return _create_parser(arg, lazy_parse)


def create_parser(arg):
    return _create_parser(arg, parse)
