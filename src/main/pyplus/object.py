from copy import copy as _copy, deepcopy as _deepcopy
from pathlib import Path as _Path

from . import table as _table
from .string import snake_case as _snake_case


class LazyObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __copy__(self):
        return self.__class__(**self.__dict__)

    def __deepcopy__(self, memo):
        kwargs = {key: _deepcopy(value) for key, value in self.__dict__.items()}
        return self.__class__(**kwargs)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.__dict__ == other
        else:
            try:
                return self.__dict__ == other.__dict__
            except AttributeError:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        params = ["%s=%s" % (key, repr(value)) for key, value in self.__dict__.items()]
        return "%s(%s)" % (self.__class__.__name__, ", ".join(params))

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, key))

    def copy(self):
        return _copy(self)

    def deepcopy(self):
        return _deepcopy(self)

    @classmethod
    def __from_table(cls, path, reader):
        if isinstance(path, (str, _Path)):
            list_ = reader(path)
            headers = {key: _snake_case(key) for key in list_[0]}
            return [cls(**{header: dict_[key] for key, header in headers.items()}) for dict_ in list_]
        else:
            raise Exception("TODO - raise better exception")

    @classmethod
    def from_csv(cls, path):
        return cls.__from_table(path, _table.csv2list)

    @classmethod
    def from_dict(cls, dict_):
        assert isinstance(dict_, dict)
        return cls(**{_snake_case(key): value for key, value in dict_.items()})

    @classmethod
    def from_list(cls, list_):
        assert isinstance(list_, list_)
        return cls(**{"_%s" % index: item for index, item in enumerate(list_)})

    @classmethod
    def from_tsv(cls, path):
        return cls.__from_table(path, _table.tsv2list)


class ImmutableLazyObject(LazyObject):
    def __setattr__(self, key, value):
        raise AttributeError("can't set attribute '%s', '%s' instances are immutable" % (key, type(self).__name__))
