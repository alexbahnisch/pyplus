#!/usr/bin/env python
from pyplus.decorators import time


@time()
def run():
    count = 0
    for i in range(1000000):
        count += i


if __name__ == "__main__":
    run()
