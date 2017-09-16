#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name="pyplus",
    version="0.0.2",
    description="A library containing a collection of python extensions.",
    url="https://github.com/alexbahnisch/pyplus",
    author="Alex Bahnisch",
    author_email="alexbahnisch@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    keywords="collection extensions plus python",
    packages=find_packages("src/main"),
    package_dir={"": "src/main"},
    install_requires=[
        "future>=0.16.0"
    ],
    tests_require=[
        "pytest>=3.2.2",
        "pytest-runner>=2.11.1"
    ],
    test_suite="src.tests"
)
