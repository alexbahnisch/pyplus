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
