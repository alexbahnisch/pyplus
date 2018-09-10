A collection of common helper functions.

## isintlike(value)
Checks if an object can be converted to an integer.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*: Returns if value can be converted to an integer.

### usage
```python
from pyplus.common import isintlike

isintlike(1)
# -> True
isintlike(True)
# -> True
isintlike(1.5)
# -> True
isintlike("1")
# -> True

isintlike("1.5")
# -> False
isintlike("one")
# -> False
isintlike("inf")
# -> False
```
## isiterable(value, include_strings=True)
Checks if an object is iterable.

#### arguments
* **value** *{object}*: The value to check.
* **include_strings** *{bool}*: Include strings as an iterable type.

#### return
* *{bool}*: Returns if value can be iterated.

### usage
```python
from pyplus.common import isiterable

isiterable((0,))
# -> True
isiterable([0])
# -> True
isiterable({"key": "value"})
# -> True
isiterable("string")
# -> True

isiterable(1)
# -> False
isiterable("string", include_strings=False)
# -> False
```
## islistlike(value)
Checks if an object has list like properties, i.e has a length, is iterable, can get and set items.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*

## ismappable(value)
Checks if an object is mappable, i.e can be passed into a 'dict' constructor.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*

## isnumber(value)
Checks if an object is a number, excludes booleans.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*

## ispair(value)
Checks if an object is a pair, i.e is iterable and has a length of 2.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*

## ispathlike(value)
Checks if an object has path like properties, i.e. is an instance of a string or pathlib.Path.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*

## issequence(value)
Checks if an object has a length and is iterable.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*

## istuplike(value)
Checks if an object has tuple like properties, i.e has a length, is iterable and can get items.

#### arguments
* **value** *{object}*: The value to check.

#### return
* *{bool}*

## iswindows()
Checks if the current operating system is windows.

#### return
* *{bool}*

