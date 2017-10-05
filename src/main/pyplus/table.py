from csv import reader as _reader, writer as _writer
from .json import Array, Object
from .parse import create_parser as _create_parser
from .path import LazyPath as _LazyPath


def table2list(path, headers=True, parse=True, delimiter=","):
    path, headers, parser = _LazyPath(str(path)), bool(headers), _create_parser(parse)
    array = Array()

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
                    array.append(obj)

        else:
            for row_index, row in enumerate(csv_reader):
                obj = Object()
                for col_index, cell in enumerate(row):
                    obj[col_index] = parser(cell)
                array.append(obj)

        return array


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
