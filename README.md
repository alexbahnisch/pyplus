# py+

*If it is not standard than it is a plus*

[![PyPI version](https://badge.fury.io/py/pyplus.svg)](https://pypi.org/project/pyplus/)
[![Development Status](https://img.shields.io/pypi/status/pyplus.svg)](https://pypi.org/project/pyplus/)
[![Python version](https://img.shields.io/pypi/pyversions/pyplus.svg)](https://pypi.org/project/pyplus/)
[![License](https://img.shields.io/pypi/l/pyplus.svg)](https://pypi.org/project/pyplus/)
[![Travis Status](https://travis-ci.org/alexbahnisch/pyplus.svg?branch=master)](https://travis-ci.org/alexbahnisch/pyplus)
[![AppVeyor Status](https://ci.appveyor.com/api/projects/status/upqpx9g2ssxbugu0/branch/master?svg=true)](https://ci.appveyor.com/project/alexbahnisch/pyplus)
[![Coveralls Coverage](https://coveralls.io/repos/github/alexbahnisch/pyplus/badge.svg)](https://coveralls.io/github/alexbahnisch/pyplus)
[![Code Climate](https://codeclimate.com/github/alexbahnisch/pyplus/badges/gpa.svg)](https://codeclimate.com/github/alexbahnisch/pyplus)
[![Issue Count](https://codeclimate.com/github/alexbahnisch/pyplus/badges/issue_count.svg)](https://codeclimate.com/github/alexbahnisch/pyplus/issues)

A python library containing a collection of nice to have python extensions, utilities and wrappers.

### Installation

```bash
$ pip install pyplus
```

### Basic Usage

```python
from pyplus.string import snake_case

snake_case("Hello World!")

# 'hello_world'
```

[comment]: <> (DocsUrlPlacemarker)

### Development

To setup the `pyplus` project for development, follow these steps from the root of the project:

```bash
$ make venv
$ make install
```

Then to run the tests:

```bash
$ make test
```

Or to run test for multiple python version with tox, run:

```bash
$ make tox
```

### Nomenclature

* `Easy` a group of extensions/utilities that are design to do a lot with minimal effort. Because of the intended 
easiness of the classes and functions they do take control away from the programmer, and may have some undesired side 
effects e.g. `pyplus.path.EasyPath` automatically creates non-existent parent directories on `touch`. 

### From the Developer

*I am a developer/data scientist creating software solutions for real world business problems. I developed `pyplus` to 
encapsulate the python code I found my self migrating from project to project. `pyplus` is pure python and has zero 
installation dependencies. My goal is for `pyplus` to be a stable library for both rapid prototyping and production 
software, though I recommend care full consideration of the `Easy` extensions in the later.*
