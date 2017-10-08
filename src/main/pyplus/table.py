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


def list2table(path, list_, headers=True, delimiter=","):
    path, headers = _LazyPath(path), bool(headers)

    with path.write() as write_file:
        csv_writer = _writer(write_file, delimiter=delimiter, lineterminator="\n")

        if len(list_) > 0:
            keys, rows = _list2table(list_)

            if headers:
                csv_writer.writerow(keys)

            for row in rows:
                csv_writer.writerow(row)
