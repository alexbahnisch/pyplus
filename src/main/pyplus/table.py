"""
A collection of table functions for reading, parsing and writing delimited text files.
"""
from csv import reader as _reader, writer as _writer
from .json import Array, Object
from .parse import create_parser as _create_parser
from .path import LazyPath as _LazyPath


def _table2list_with_headers(csv_reader, parser):
    array, keys = Array(), []

    for row_index, row in enumerate(csv_reader):

        if row_index == 0:
            keys = list(row)

        else:
            obj = Object()
            for col_index, cell in enumerate(row):
                obj[keys[col_index]] = parser(cell)
            array.append(obj)

    return array


def _table2list_without_headers(csv_reader, parser):
    array = Array()

    for row_index, row in enumerate(csv_reader):
        obj = Object()
        for col_index, cell in enumerate(row):
            obj[col_index] = parser(cell)
        array.append(obj)

    return array


def table2list(path, headers=True, parse=True, delimiter=","):
    """
    Read data from a delimited txt file to an pyplus.json.Array (subclass of list) of pyplus.json.Objects (subclass of dict).
    @param path: {string or path} Path of delimited text file to read from.
    @param headers: {bool} Does table have headers, if true, the object keys will be the column headers, if false, the object keys will be the row column index.
    @param parse: {bool or (value: string) -> any} Should the values be parsed, or supply a parser function to parse all values.
    @param delimiter: {string} Delimiter to separate values by.
    @return: {pyplus.json.Array}
    """
    path, parser = _LazyPath(path), _create_parser(parse)

    with path.read() as read_file:
        csv_reader = _reader(read_file, delimiter=delimiter)

        if headers:
            return _table2list_with_headers(csv_reader, parser)
        else:
            return _table2list_without_headers(csv_reader, parser)


def _list2table(list_):
    keys, rows = [], []

    for item in list_:
        for key in item:
            if key not in keys:
                keys.append(key)

        rows.append([item.get(key, "") for key in keys])

    return keys, rows


def list2table(path, array, headers=True, delimiter=","):
    """
    Write data from a list of dictionaries to a delimited txt file.
    @param path: {string or path} Path of delimited text file to read from.
    @param array: {list} List of dictionaries to write to file.
    @param headers: {bool} Include dictionary keys as column headers.
    @param delimiter: {string} Delimiter to separate values by.
    """
    path = _LazyPath(path)

    with path.write() as write_file:
        csv_writer = _writer(write_file, delimiter=delimiter, lineterminator="\n")

        if len(array) > 0:
            keys, rows = _list2table(array)

            if headers:
                csv_writer.writerow(keys)

            for row in rows:
                csv_writer.writerow(row)
