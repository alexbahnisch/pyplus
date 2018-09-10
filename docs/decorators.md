A collection of useful decorators.

## parser(method)
Decorator for a string parsing function.
Raises 'TypeError' if the first and only positional arg is not a string.
Also guarantees if return value is a string, it is the same string as the input arg, i.e. byte or unicode.

#### arguments
* **method** *{function}*: Parser function, contains one positional arg and any number of keyword args.

#### return
* *{function}*: Wrapped parser function.

