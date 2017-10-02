#!/usr/bin/env python
from pyplus.json import Array, Object
from pyplus.path import LazyPath
from pyplus.table import dict2table, list2table, table2dict, table2list

DIR = LazyPath(__file__)
CSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/csv/headers.csv")
CSV_HEADERS_OUTPUT = LazyPath(DIR.parent, "../resources/csv/headers.output.csv")
CSV_HEADERS_TEMP = LazyPath(DIR.parent, "../resources/csv/headers.temp.csv")

CSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/csv/headless.csv")
CSV_HEADLESS_OUTPUT = LazyPath(DIR.parent, "../resources/csv/headless.output.csv")
CSV_HEADLESS_TEMP = LazyPath(DIR.parent, "../resources/csv/headless.temp.csv")

TSV_HEADERS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headers.tsv")
TSV_HEADERS_OUTPUT = LazyPath(DIR.parent, "../resources/tsv/headers.output.tsv")
TSV_HEADERS_TEMP = LazyPath(DIR.parent, "../resources/tsv/headers.temp.tsv")

TSV_HEADLESS_INPUT = LazyPath(DIR.parent, "../resources/tsv/headless.tsv")
TSV_HEADLESS_OUTPUT = LazyPath(DIR.parent, "../resources/tsv/headless.output.tsv")
TSV_HEADLESS_TEMP = LazyPath(DIR.parent, "../resources/tsv/headless.temp.tsv")

HEADERS_DICT = Object({
    "bool": Array([False, False, True, True, True, True, True, False, True, True]),
    "int": Array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    "float": Array(
        [3.387182583, 4.523252832, 1.577410661, 0.861610127, 1.461357371, 1.907316961, 1.214172801, 2.010788362,
         1.91548151, 0.785592075]),
    "string": Array(["boring", "royal", "want", "communicate", "perfect", "crack", "ragged", "scribble", "obnoxious",
                     "incandescent"]),
    "null": Array([None, None, None, None, None, None, None, None, None, None])
})

HEADLESS_DICT = Object({
    0: Array([False, False, True, True, True, True, True, False, True, True]),
    1: Array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    2: Array([3.387182583, 4.523252832, 1.577410661, 0.861610127, 1.461357371, 1.907316961, 1.214172801, 2.010788362,
              1.91548151, 0.785592075]),
    3: Array(["boring", "royal", "want", "communicate", "perfect", "crack", "ragged", "scribble", "obnoxious",
              "incandescent"]),
    4: Array([None, None, None, None, None, None, None, None, None, None])
})

NO_PARSE_DICT = Object({
    "bool": Array(["FALSE", "FALSE", "TRUE", "TRUE", "TRUE", "TRUE", "TRUE", "FALSE", "TRUE", "TRUE"]),
    "string": Array(["boring", "royal", "want", "communicate", "perfect", "crack", "ragged", "scribble", "obnoxious",
                     "incandescent"]),
    "float": Array(
        ["3.387182583", "4.523252832", "1.577410661", "0.861610127", "1.461357371", "1.907316961", "1.214172801",
         "2.010788362", "1.91548151", "0.785592075"]),
    "null": Array(["", "", "#N/A", "#N/A", "None", "None", "null", "null", "undefined", "undefined"]),
    "int": Array(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
})

HEADERS_LIST = Array([
    Object({'float': 3.387182583, 'int': 1, 'null': None, 'string': 'boring', 'bool': False}),
    Object({'float': 4.523252832, 'int': 2, 'null': None, 'string': 'royal', 'bool': False}),
    Object({'float': 1.577410661, 'int': 3, 'null': None, 'string': 'want', 'bool': True}),
    Object({'float': 0.861610127, 'int': 4, 'null': None, 'string': 'communicate', 'bool': True}),
    Object({'float': 1.461357371, 'int': 5, 'null': None, 'string': 'perfect', 'bool': True}),
    Object({'float': 1.907316961, 'int': 6, 'null': None, 'string': 'crack', 'bool': True}),
    Object({'float': 1.214172801, 'int': 7, 'null': None, 'string': 'ragged', 'bool': True}),
    Object({'float': 2.010788362, 'int': 8, 'null': None, 'string': 'scribble', 'bool': False}),
    Object({'float': 1.91548151, 'int': 9, 'null': None, 'string': 'obnoxious', 'bool': True}),
    Object({'float': 0.785592075, 'int': 10, 'null': None, 'string': 'incandescent', 'bool': True})
])

HEADLESS_LIST = Array([
    Object({'0': False, '2': 3.387182583, '3': 'boring', '4': None, '1': 1}),
    Object({'0': False, '2': 4.523252832, '3': 'royal', '4': None, '1': 2}),
    Object({'0': True, '2': 1.577410661, '3': 'want', '4': None, '1': 3}),
    Object({'0': True, '2': 0.861610127, '3': 'communicate', '4': None, '1': 4}),
    Object({'0': True, '2': 1.461357371, '3': 'perfect', '4': None, '1': 5}),
    Object({'0': True, '2': 1.907316961, '3': 'crack', '4': None, '1': 6}),
    Object({'0': True, '2': 1.214172801, '3': 'ragged', '4': None, '1': 7}),
    Object({'0': False, '2': 2.010788362, '3': 'scribble', '4': None, '1': 8}),
    Object({'0': True, '2': 1.91548151, '3': 'obnoxious', '4': None, '1': 9}),
    Object({'0': True, '2': 0.785592075, '3': 'incandescent', '4': None, '1': 10})
])

NO_PARSE_LIST = Array([
    Object({'bool': 'FALSE', 'string': 'boring', 'null': '', 'float': '3.387182583', 'int': '1'}),
    Object({'bool': 'FALSE', 'string': 'royal', 'null': '', 'float': '4.523252832', 'int': '2'}),
    Object({'bool': 'TRUE', 'string': 'want', 'null': '#N/A', 'float': '1.577410661', 'int': '3'}),
    Object({'bool': 'TRUE', 'string': 'communicate', 'null': '#N/A', 'float': '0.861610127', 'int': '4'}),
    Object({'bool': 'TRUE', 'string': 'perfect', 'null': 'None', 'float': '1.461357371', 'int': '5'}),
    Object({'bool': 'TRUE', 'string': 'crack', 'null': 'None', 'float': '1.907316961', 'int': '6'}),
    Object({'bool': 'TRUE', 'string': 'ragged', 'null': 'null', 'float': '1.214172801', 'int': '7'}),
    Object({'bool': 'FALSE', 'string': 'scribble', 'null': 'null', 'float': '2.010788362', 'int': '8'}),
    Object({'bool': 'TRUE', 'string': 'obnoxious', 'null': 'undefined', 'float': '1.91548151', 'int': '9'}),
    Object({'bool': 'TRUE', 'string': 'incandescent', 'null': 'undefined', 'float': '0.785592075', 'int': '10'})
])


def test_csv2dict():
    dict_ = table2dict(CSV_HEADERS_INPUT)
    assert HEADERS_DICT == dict_
    assert HEADERS_DICT is not dict_
    dict2table(CSV_HEADERS_TEMP, dict_)
    assert CSV_HEADERS_OUTPUT.read_text() == CSV_HEADERS_TEMP.read_text()

    dict_ = table2dict(CSV_HEADLESS_INPUT, headers=False)
    assert HEADLESS_DICT == dict_
    assert HEADLESS_DICT is not dict_
    dict2table(CSV_HEADLESS_TEMP, dict_, headers=False)
    assert CSV_HEADLESS_OUTPUT.read_text() == CSV_HEADLESS_TEMP.read_text()

    dict_ = table2dict(CSV_HEADERS_INPUT, parse=False)
    assert NO_PARSE_DICT == dict_
    assert NO_PARSE_DICT is not dict_


def test_tsv2dict():
    dict_ = table2dict(TSV_HEADERS_INPUT, delimiter="\t")
    assert HEADERS_DICT == dict_
    assert HEADERS_DICT is not dict_
    dict2table(TSV_HEADERS_TEMP, dict_, delimiter="\t")
    assert TSV_HEADERS_OUTPUT.read_text() == TSV_HEADERS_TEMP.read_text()

    dict_ = table2dict(TSV_HEADLESS_INPUT, delimiter="\t", headers=False)
    assert HEADLESS_DICT == dict_
    assert HEADLESS_DICT is not dict_
    dict2table(TSV_HEADLESS_TEMP, dict_, delimiter="\t", headers=False)
    assert TSV_HEADLESS_OUTPUT.read_text() == TSV_HEADLESS_TEMP.read_text()

    dict_ = table2dict(TSV_HEADERS_INPUT, delimiter="\t", parse=False)
    assert NO_PARSE_DICT == dict_
    assert NO_PARSE_DICT is not dict_


def test_csv2list():
    list_ = table2list(CSV_HEADERS_INPUT)
    assert HEADERS_LIST == list_
    assert HEADERS_LIST is not list_
    list2table(CSV_HEADERS_TEMP, list_)
    assert CSV_HEADERS_OUTPUT.read_text() == CSV_HEADERS_TEMP.read_text()

    list_ = table2list(CSV_HEADLESS_INPUT, headers=False)
    assert HEADLESS_LIST == list_
    assert HEADLESS_LIST is not list_
    list2table(CSV_HEADLESS_TEMP, list_, headers=False)
    assert CSV_HEADLESS_OUTPUT.read_text() == CSV_HEADLESS_TEMP.read_text()

    list_ = table2list(CSV_HEADERS_INPUT, parse=False)
    assert NO_PARSE_LIST == list_
    assert NO_PARSE_LIST is not list_


def test_tsv2list():
    list_ = table2list(TSV_HEADERS_INPUT, delimiter="\t")
    assert HEADERS_LIST == list_
    assert HEADERS_LIST is not list_
    list2table(TSV_HEADERS_TEMP, list_, delimiter="\t")
    assert TSV_HEADERS_OUTPUT.read_text() == TSV_HEADERS_TEMP.read_text()

    list_ = table2list(TSV_HEADLESS_INPUT, delimiter="\t", headers=False)
    assert HEADLESS_LIST == list_
    assert HEADLESS_LIST is not list_
    list2table(TSV_HEADLESS_TEMP, list_, delimiter="\t", headers=False)
    assert TSV_HEADLESS_OUTPUT.read_text() == TSV_HEADLESS_TEMP.read_text()

    list_ = table2list(TSV_HEADERS_INPUT, delimiter="\t", parse=False)
    assert NO_PARSE_LIST == list_
    assert NO_PARSE_LIST is not list_
