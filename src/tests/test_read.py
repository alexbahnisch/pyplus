#!/usr/bin/env python
from pyplus.path import LazyPath
from pyplus.read import *


DIR = LazyPath(__file__)
CSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/csv/headers.csv")
CSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/csv/headless.csv")
TSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headers.tsv")
TSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headless.tsv")

HEADERS_DICT = {
    "bool": [False, False, True, True, True, True, True, False, True, True],
    "int": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "float": [3.387182583, 4.523252832, 1.577410661, 0.861610127, 1.461357371, 1.907316961, 1.214172801, 2.010788362, 1.91548151, 0.785592075],
    "string": ["boring", "royal", "want", "communicate", "perfect", "crack", "ragged", "scribble", "obnoxious", "incandescent"],
    "null": [None, None, None, None, None, None, None, None, None, None]
}

HEADLESS_DICT = {
    0: [False, False, True, True, True, True, True, False, True, True],
    1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    2: [3.387182583, 4.523252832, 1.577410661, 0.861610127, 1.461357371, 1.907316961, 1.214172801, 2.010788362, 1.91548151, 0.785592075],
    3: ["boring", "royal", "want", "communicate", "perfect", "crack", "ragged", "scribble", "obnoxious", "incandescent"],
    4: [None, None, None, None, None, None, None, None, None, None]
}

NO_PARSE_DICT = {
    "bool": ["FALSE", "FALSE", "TRUE", "TRUE", "TRUE", "TRUE", "TRUE", "FALSE", "TRUE", "TRUE"],
    "string": ["boring", "royal", "want", "communicate", "perfect", "crack", "ragged", "scribble", "obnoxious", "incandescent"],
    "float": ["3.387182583", "4.523252832", "1.577410661", "0.861610127", "1.461357371", "1.907316961", "1.214172801", "2.010788362", "1.91548151", "0.785592075"],
    "null": ["", "", "#N/A", "#N/A", "None", "None", "null", "null", "undefined", "undefined"],
    "int": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
}

HEADERS_LIST = [
    {'float': 3.387182583, 'int': 1, 'null': None, 'string': 'boring', 'bool': False},
    {'float': 4.523252832, 'int': 2, 'null': None, 'string': 'royal', 'bool': False},
    {'float': 1.577410661, 'int': 3, 'null': None, 'string': 'want', 'bool': True},
    {'float': 0.861610127, 'int': 4, 'null': None, 'string': 'communicate', 'bool': True},
    {'float': 1.461357371, 'int': 5, 'null': None, 'string': 'perfect', 'bool': True},
    {'float': 1.907316961, 'int': 6, 'null': None, 'string': 'crack', 'bool': True},
    {'float': 1.214172801, 'int': 7, 'null': None, 'string': 'ragged', 'bool': True},
    {'float': 2.010788362, 'int': 8, 'null': None, 'string': 'scribble', 'bool': False},
    {'float': 1.91548151, 'int': 9, 'null': None, 'string': 'obnoxious', 'bool': True},
    {'float': 0.785592075, 'int': 10, 'null': None, 'string': 'incandescent', 'bool': True}
]

HEADLESS_LIST = [
    [False, 1, 3.387182583, 'boring', None],
    [False, 2, 4.523252832, 'royal', None],
    [True, 3, 1.577410661, 'want', None],
    [True, 4, 0.861610127, 'communicate', None],
    [True, 5, 1.461357371, 'perfect', None],
    [True, 6, 1.907316961, 'crack', None],
    [True, 7, 1.214172801, 'ragged', None],
    [False, 8, 2.010788362, 'scribble', None],
    [True, 9, 1.91548151, 'obnoxious', None],
    [True, 10, 0.785592075, 'incandescent', None]
]

NO_PARSE_LIST = [
    {'bool': 'FALSE', 'string': 'boring', 'null': '', 'float': '3.387182583', 'int': '1'},
    {'bool': 'FALSE', 'string': 'royal', 'null': '', 'float': '4.523252832', 'int': '2'},
    {'bool': 'TRUE', 'string': 'want', 'null': '#N/A', 'float': '1.577410661', 'int': '3'},
    {'bool': 'TRUE', 'string': 'communicate', 'null': '#N/A', 'float': '0.861610127', 'int': '4'},
    {'bool': 'TRUE', 'string': 'perfect', 'null': 'None', 'float': '1.461357371', 'int': '5'},
    {'bool': 'TRUE', 'string': 'crack', 'null': 'None', 'float': '1.907316961', 'int': '6'},
    {'bool': 'TRUE', 'string': 'ragged', 'null': 'null', 'float': '1.214172801', 'int': '7'},
    {'bool': 'FALSE', 'string': 'scribble', 'null': 'null', 'float': '2.010788362', 'int': '8'},
    {'bool': 'TRUE', 'string': 'obnoxious', 'null': 'undefined', 'float': '1.91548151', 'int': '9'},
    {'bool': 'TRUE', 'string': 'incandescent', 'null': 'undefined', 'float': '0.785592075', 'int': '10'}
]


def test_csv2dict():
    dict_ = csv2dict(CSV_HEADERS_INPUT)
    assert HEADERS_DICT == dict_
    assert HEADERS_DICT is not dict_

    dict_ = csv2dict(CSV_HEADLESS_INPUT, headers=False)
    assert HEADLESS_DICT == dict_
    assert HEADLESS_DICT is not dict_

    dict_ = csv2dict(CSV_HEADERS_INPUT, parse=False)
    assert NO_PARSE_DICT == dict_
    assert NO_PARSE_DICT is not dict_


def test_tsv2dict():
    dict_ = tsv2dict(TSV_HEADERS_INPUT)
    assert HEADERS_DICT == dict_
    assert HEADERS_DICT is not dict_

    dict_ = tsv2dict(TSV_HEADLESS_INPUT, headers=False)
    assert HEADLESS_DICT == dict_
    assert HEADLESS_DICT is not dict_

    dict_ = tsv2dict(TSV_HEADERS_INPUT, parse=False)
    assert NO_PARSE_DICT == dict_
    assert NO_PARSE_DICT is not dict_


def test_csv2list():
    list_ = csv2list(CSV_HEADERS_INPUT)
    assert HEADERS_LIST == list_
    assert HEADERS_LIST is not list_

    list_ = csv2list(CSV_HEADLESS_INPUT, headers=False)
    assert HEADLESS_LIST == list_
    assert HEADLESS_LIST is not list_

    list_ = csv2list(CSV_HEADERS_INPUT, parse=False)
    assert NO_PARSE_LIST == list_
    assert NO_PARSE_LIST is not list_


def test_tsv2list():
    list_ = tsv2list(TSV_HEADERS_INPUT)
    assert HEADERS_LIST == list_
    assert HEADERS_LIST is not list_

    list_ = tsv2list(TSV_HEADLESS_INPUT, headers=False)
    assert HEADLESS_LIST == list_
    assert HEADLESS_LIST is not list_

    list_ = tsv2list(TSV_HEADERS_INPUT, parse=False)
    assert NO_PARSE_LIST == list_
    assert NO_PARSE_LIST is not list_
