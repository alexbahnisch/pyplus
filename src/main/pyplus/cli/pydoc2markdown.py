#!/usr/bin/env python3
from argparse import ArgumentParser
from inspect import getmembers, isclass, isfunction, ismethod, signature
from os import getcwd
# noinspection PyProtectedMember
from pydoc import ErrorDuringImport, safeimport
from sys import path

from pyplus.path import LazyPath
from pyplus.string import extract_between

MODULE_FORMAT = "# {}"
CLASS_FORMAT = "## {}"
FUNCTION_FORMAT = "## {}"
METHOD_FORMAT = "### {}"
PARAMETERS_HEADER = "#### arguments"
RETURN_HEADER = "#### return"
USAGE_HEADER = "### usage"

DEPRECATED = "@deprecated"
PARAM = "@param"
RETURN = "@return"


def prettify_line(line):
    name, line = extract_between(line.strip(), "", ":")
    type_, line = extract_between(line, "{", "}")
    rarg = ""

    if name:
        rarg += " **{}**".format(name)

    if type_:
        rarg += " *{" + type_ + "}*"

    if line and rarg:
        rarg += ": "

    if line:
        rarg += line.strip()

    return "*{}".format(rarg).strip()


def get_predicate(mod):
    """
    Creates a predicate function for the inspect.getmembers function.
    The created function will excepts a single arg and returns true if that
    arg is a class, function or method defined within the "module_" module.
    @param mod: {module or str} python module
    @return: {function} predicate function
    """
    if isinstance(mod, str):
        module_name = mod
    else:
        module_name = mod.__name__

    def predicate(value):
        return (isclass(value) or isfunction(value) or ismethod(value)) and value.__module__ == module_name

    return predicate


def member2markdown(name, usages, value, title_format):
    """
    Creates the markdown for a member of the modules.
    @param name: {str} name of member
    @param usages: {dict} value of member
    @param value: {any} value of member
    @param title_format: {str} formatted string for the title of the member
    @return: {list} list of markdown strings
    """
    output, prefix, params, returns = [], [], [], []

    if value.__doc__ is not None:
        previous_was_param = False
        previous_was_return = False
        output.append(title_format.format(name) + str(signature(value)))
        for line in value.__doc__.split("\n")[1:]:
            line = line.replace("__", "\_\_").strip()
            if DEPRECATED in line:
                return []
            elif PARAM in line:
                previous_was_param, previous_was_return = True, False
                params.append(prettify_line(line.replace(PARAM, "")))
            elif RETURN in line:
                previous_was_param, previous_was_return = False, True
                returns.append(prettify_line(line.replace(RETURN, "")))
            elif previous_was_param:
                params.append(line)
            elif previous_was_return:
                returns.append(line)
            else:
                prefix.append(line)

        if prefix:
            output.extend([pre for pre in prefix])

        if params:
            if prefix:
                output.append("")

            output.append(PARAMETERS_HEADER)
            output.extend(params)

        if returns:
            if prefix or params:
                output.append("")

            output.append(RETURN_HEADER)
            output.extend(returns)

        if name in usages:
            output.append(USAGE_HEADER)
            output.append("```python")
            with usages[name].read() as usage:
                for line in usage:
                    output.append(line.replace("\n", ""))
            output.append("```")

    return output


def class2markdown(name, usages, value):
    cls, methods, output = member2markdown(name, usages, value, CLASS_FORMAT), [], []

    for name, value in getmembers(value, get_predicate(value.__module__)):
        if name[0] != "_":
            methods.extend(
                member2markdown(name, usages, value, METHOD_FORMAT)
            )

    if not cls and methods:
        cls.extend(
            [CLASS_FORMAT.format(name), ""]
        )

    return [*cls, *methods]


def module2markdown(module_, title, usage_dir):
    output = []
    usages = {usage.stem: usage for usage in usage_dir if usage.is_file() and usage.suffix == ".py"}

    if title:
        output.append(MODULE_FORMAT.format(module_.__name__))

    if module_.__doc__:
        output.extend(module_.__doc__.split("\n")[1:])

    for name, value in getmembers(module_, get_predicate(module_)):
        if isfunction(value) and name[0] != "_":
            output.extend(
                member2markdown(name, usages, value, FUNCTION_FORMAT)
            )
        elif isclass(value) and name[0] != "_":
            output.extend(
                class2markdown(name, usages, value)
            )

    return output


def pydoc2markdown(**args):
    try:
        path.append(getcwd())
        mod = safeimport(args["module"])
        if mod is None:
            print("{} module not found".format(mod))

        markdown = module2markdown(mod, args["title"], args["usage_dir"])

        if args["output"]:
            with args["output"].write() as output:
                for line in markdown:
                    output.write(line)
                    output.write("\n")
        else:
            for line in markdown:
                print(line)

    except ErrorDuringImport:
        print("Error while importing {}".format(args["module"]))


def main():
    parser = ArgumentParser(description="Convert python (pycharm Epytext) docstrings to markdown")
    parser.add_argument("module", type=str)
    parser.add_argument("-o", "--output", type=LazyPath)
    parser.add_argument("-t", "--title", default=False, type=bool)
    parser.add_argument("-u", "--usage-dir", type=LazyPath)
    args, _ = parser.parse_known_args()
    pydoc2markdown(**vars(args))


if __name__ == "__main__":
    main()
