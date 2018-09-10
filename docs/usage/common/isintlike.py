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
