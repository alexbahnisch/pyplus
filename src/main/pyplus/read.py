from csv import reader as _reader
from collections import defaultdict

from .parse import create_parser as _create_parser
from .path import LazyPath as _LazyPath


def _csv2dict(path, headers, parse, delimiter):
    path, headers, parser = _LazyPath(path), bool(headers), _create_parser(parse)
    dict_ = defaultdict(list)

    with path.read() as read_file:
        csv_reader = _reader(read_file, delimiter=delimiter)

        if headers:
            for row_index, row in enumerate(csv_reader):

                if row_index == 0:
                    headers = list(row)

                else:
                    for col_index, cell in enumerate(row):
                        dict_[headers[col_index]].append(parser(cell))

        else:
            for row_index, row in enumerate(csv_reader):
                for col_index, cell in enumerate(row):
                    dict_[col_index].append(parser(cell))

        return dict(dict_)


def _csv2list(path, headers=True, parser=True, delimiter=","):
    path, headers, parser = _LazyPath(str(path)), bool(headers), _create_parser(parser)
    list_ = list()

    with path.open("r") as read_file:
        csv_reader = _reader(read_file, delimiter=delimiter)

        if headers:
            for row_index, row in enumerate(csv_reader):

                if row_index == 0:
                    headers = list(row)

                else:
                    list_.append({headers[col_index]: parser(cell) for col_index, cell in enumerate(row)})

        else:
            for row_index, row in enumerate(csv_reader):
                list_.append([parser(cell) for cell in row])

        return list_


def csv2dict(path, headers=True, parse=True):
    return _csv2dict(path, headers, parse, ",")


def csv2list(path, headers=True, parse=True):
    return _csv2list(path, headers, parse, ",")


def tsv2dict(path, headers=True, parse=True):
    return _csv2dict(path, headers, parse, "\t")


def tsv2list(path, headers=True, parse=True):
    return _csv2list(path, headers, parse, "\t")
