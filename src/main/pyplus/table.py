from csv import reader as _reader, writer as _writer
from .json import Array, Object
from .parse import create_parser as _create_parser
from .path import LazyPath as _LazyPath


def table2dict(path, headers, parse, delimiter):
    path, headers, parser = _LazyPath(path), bool(headers), _create_parser(parse)
    dict_ = Object()

    with path.read() as read_file:
        csv_reader = _reader(read_file, delimiter=delimiter)

        if headers:
            keys = []
            for row_index, row in enumerate(csv_reader):

                if row_index == 0:
                    keys.extend(row)
                    for key in keys:
                        dict_[key] = Array()

                else:
                    for col_index, cell in enumerate(row):
                        dict_[keys[col_index]][row_index - 1] = parser(cell)

        else:
            for row_index, row in enumerate(csv_reader):

                if row_index == 0:
                    for col_index, cell in enumerate(row):
                        dict_[col_index] = Array([parser(cell)])

                else:
                    for col_index, cell in enumerate(row):
                        dict_[col_index][row_index] = parser(cell)

        return dict_


def table2list(path, headers=True, parser=True, delimiter=","):
    path, headers, parser = _LazyPath(str(path)), bool(headers), _create_parser(parser)
    list_ = Array()

    with path.read() as read_file:
        csv_reader = _reader(read_file, delimiter=delimiter)

        if headers:
            for row_index, row in enumerate(csv_reader):

                if row_index == 0:
                    headers = list(row)

                else:
                    obj = Object()
                    for col_index, cell in enumerate(row):
                        obj[headers[col_index]] = parser(cell)
                    list_.append(obj)

        else:
            for row_index, row in enumerate(csv_reader):
                obj = Object()
                for col_index, cell in enumerate(row):
                    obj[col_index] = parser(cell)
                list_.append(obj)

        return list_


def csv2dict(path, headers=True, parse=True):
    return table2dict(path, headers, parse, ",")


def csv2list(path, headers=True, parse=True):
    return table2list(path, headers, parse, ",")


def dict2table(path, dict_, headers=True, delimiter=","):
    path, headers = _LazyPath(path), bool(headers)

    with path.write() as write_file:
        csv_writer = _writer(write_file, delimiter=delimiter, lineterminator="\n")

        if headers:
            csv_writer.writerow(dict_.keys())

        for row in zip(*[value for value in dict_.values()]):
            csv_writer.writerow(row)


def dict2csv(path, dict_, headers=True):
    return dict2table(path, dict_, headers, ",")


def dict2tsv(path, dict_, headers=True):
    return dict2table(path, dict_, headers, "\t")


def list2table(path, list_, headers=True, delimiter=","):
    path, headers = _LazyPath(path), bool(headers)

    with path.write() as write_file:
        csv_writer = _writer(write_file, delimiter=delimiter, lineterminator="\n")

        if len(list_) > 0:
            keys, rows = [], []

            for item in list_:
                for key in item:
                    if key not in keys:
                        keys.append(key)

                rows.append([item.get(key, "") for key in keys])

            if headers:
                csv_writer.writerow(keys)

            for row in rows:
                csv_writer.writerow(row)


def list2csv(path, list_, headers=True):
    return list2table(path, list_, headers, ",")


def list2tsv(path, list_, headers=True):
    return list2table(path, list_, headers, "\t")


def tsv2dict(path, headers=True, parse=True):
    return table2dict(path, headers, parse, "\t")


def tsv2list(path, headers=True, parse=True):
    return table2list(path, headers, parse, "\t")
