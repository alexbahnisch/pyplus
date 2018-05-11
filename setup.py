#!/usr/bin/env python
from sys import argv
from setuptools import find_packages, setup

long_description = "!!! pypandoc and/or pandoc not found, long_description is bad, don't upload this to PyPI !!!"

if any(arg in argv for arg in ["sdist", "bdist_wheel"]):
    try:
        # noinspection PyPackageRequirements, PyUnresolvedReferences
        # from pypandoc import convert, download_pandoc
        #
        # download_pandoc()
        # long_description = convert("README.md", "rst")

        with open("README.md") as file:
            long_description = file.read()

    except (ImportError, OSError):
        pass

setup(
    name="pyplus",
    version="0.1.7.dev0",
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
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    keywords="collection extensions plus python",
    packages=find_packages("src/main"),
    package_dir={"": "src/main"},
    python_requires=">=3.5",
    extras_require={
        "dist": [
            "pypandoc>=1.4<2"
        ],
        "docs": [
            "mkdocs>=0.17.3<1",
            "mkdocs-material>=2.7.3<3"
        ],
        "tests": [
            "coverage>=4.4.2<5",
            "pytest>=3.2.2<4",
            "pytest-runner>=2.11.1<3",
            "tox>=2.9.1<3"
        ]
    },
    test_suite="src.tests"
)
