#!/bin/python
from argparse import ArgumentParser
from inspect import getmembers, isclass, isfunction, ismethod
from os import getcwd
from pydoc import ErrorDuringImport, safeimport
from sys import path

MODULE_FORMAT = "# *module* %s"
CLASS_FORMAT = "## *class* %s"
FUNCTION_FORMAT = "## *function* %s"
METHOD_FORMAT = "### *method* %s"
PARAMETERS_FORMAT = "**Parameters:**"
RETURN_FORMAT = "**Return:**"

PARAM = "@param"
RETURN = "@return"


def get_predicate(module_):
    """
    Creates a predicate function for the inspect.getmembers function.
    The created function will excepts a single arg and returns true if that
    arg is a class, function or method defined within the "module_" module.
    @param module_: {module or str} python module
    @return: {function} predicate function
    """
    if isinstance(module_, str):
        module_name = module_
    else:
        module_name = module_.__name__

    def predicate(value):
        return (isclass(value) or isfunction(value) or ismethod(value)) and value.__module__ == module_name
    return predicate


def member2markdown(name, value, title_format):
    """
    Creates the markdown for a member of the modules.
    @param name: {str} name of member
    @param value: {any} value of member
    @param title_format: {str} formatted string for the title of the member
    @return: {list} list of markdown strings
    """
    output, prefix, params, returns, suffix = [], [], [], [], []

    if value.__doc__ is not None:
        output.append(title_format % name)
        for line in value.__doc__.split("\n"):
            if PARAM in line:
                params.append(line.replace(PARAM, "*").strip())
            elif RETURN in line:
                returns.append(line.replace(RETURN, "").strip())
            elif params or returns:
                suffix.append(line.strip())
            else:
                prefix.append(line.strip())

        if prefix:
            output.extend([pre for pre in prefix])
            output.append("")

        if params:
            output.append("**Parameters:**")
            output.extend(params)
            output.append("")

        if returns:
            output.append("**Return:**")
            output.extend(returns)
            output.append("")

        if suffix:
            output.extend(suffix)
            output.append("")

    return output


def class2markdown(name, value):
    class_, methods, output = member2markdown(name, value, CLASS_FORMAT), [], []

    for name, value in getmembers(value, get_predicate(value.__module__)):
        if name[0] != "_":
            methods.extend(
                member2markdown(name, value, METHOD_FORMAT)
            )

    if not class_ and methods:
        class_.extend(
            [CLASS_FORMAT % name, ""]
        )

    return [*class_, *methods]


def module2markdown(module_):
    output = [MODULE_FORMAT % module_.__name__]

    if module_.__doc__:
        output.append(module_.__doc__)

    for name, value in getmembers(module_, get_predicate(module_)):
        if isfunction(value) and name[0] != "_":
            output.extend(
                member2markdown(name, value, FUNCTION_FORMAT)
            )
        elif isclass(value) and name[0] != "_":
            output.extend(
                class2markdown(name, value)
            )

    return "\n".join((str(x) for x in output))


def pydoc2markdown(module_):
    try:
        path.append(getcwd())
        module_ = safeimport(module_)
        if module_ is None:
            print("%s module not found" % module_)

        print(module2markdown(module_))
    except ErrorDuringImport:
        print("Error while importing %s" % module_)


if __name__ == "__main__":
    parser = ArgumentParser(description="Convert python (pycharm Epytext) docstrings to markdown")
    parser.add_argument("module", default="pydoc2markdown", type=str)
    parser.add_argument("-t", "--title", type=str)
    args, _ = parser.parse_known_args()

    pydoc2markdown(args.module)
