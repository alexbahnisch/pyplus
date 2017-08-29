#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name="pyplus",
    version="0.0.1.dev0",
    description="A python extension library.",
    url="https://github.com/alexbahnisch/python-plus",
    author="Alex Bahnisch",
    author_email="alexbahnisch@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Data Scientists",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7"
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    keywords="python boilerplate",
    packages=find_packages("src/main", exclude=["tests"]),
    package_dir={"": "src/main"},
    install_requires=[
        "future>=0.16.0"
    ],
    setup_requires=[
        "pytest-runner>=2.11.1",
        "tox>=2.7.0"
    ],
    tests_require=[
        "pytest>=3.1.3"
    ],
    test_suite="src.tests"
)
