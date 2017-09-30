from setuptools import find_packages, setup

try:
    # noinspection PyUnresolvedReferences
    from pypandoc import convert, download_pandoc

    download_pandoc()
    long_description = convert("README.md", "rst")

except (ImportError, OSError):
    long_description = "!!! pypandoc and/or pandoc not found, long_description is bad, don't upload this to PyPI !!!"

setup(
    name="pyplus",
    version="0.0.5.dev6",
    description="A library containing a collection of python extensions.",
    long_description=long_description,
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython"
    ],
    keywords="collection extensions plus python",
    packages=find_packages("src/main"),
    package_dir={"": "src/main"},
    python_requires=">=3.5",
    setup_requires=[
        "pypandoc>=1.4"
    ],
    tests_require=[
        "pytest>=3.2.2",
        "pytest-runner>=2.11.1"
    ],
    test_suite="src.tests"
)
