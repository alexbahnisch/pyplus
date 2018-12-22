#!/usr/bin/env python3
from re import sub
from sys import argv
from setuptools import find_packages, setup

long_description = "!!! m2r not found, long_description is bad, don't upload this to PyPI !!!"
appveyor = [
    "pytest>=3.7.4,<4",
    "pytest-runner>=4.2,<5",
]
dist = [
    "m2r>=0.2,<0.3"
]
docs = [
    "mkdocs>=1.0.3,<2",
    "mkdocs-material>=3.0.4,<4"
]
test = [
    "coverage>=4.5.1,<5",
    *appveyor,
    "tox>=3.2.1,<4"
]
travis = [
    "coveralls>=1.5.0,<2",
    "tox-travis>=0.10<1"
]

if any(arg in argv for arg in ["sdist", "bdist_wheel"]):
    try:
        # noinspection PyPackageRequirements
        from m2r import convert
        long_description = convert(sub("<!---.*?--->", "", open("README.md").read()))
    except (ImportError, OSError, ValueError):
        pass

setup(
    name="pyplus",
    version="0.1.5.dev0",
    description="A library containing a collection of python extensions.",
    long_description=long_description,
    url="https://github.com/alexbahnisch/pyplus",
    author="Alex Bahnisch",
    author_email="alexbahnisch@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    keywords="collection extensions plus python",
    packages=find_packages("src/main"),
    package_dir={"": "src/main"},
    python_requires=">=3.6",
    extras_require={
        "appveyor": appveyor,
        "develop": dist + docs + test,
        "dist": dist,
        "docs": docs,
        "test": test,
        "travis": travis
    },
    test_suite="src.tests",
    entry_points={
        "console_scripts": ["pydoc2markdown=pyplus.cli.pydoc2markdown:main"],
    }
)
