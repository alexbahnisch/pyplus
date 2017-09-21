from copy import deepcopy as _deepcopy

from . import read as _io
from .string import snake_case as _snake_case


class LazyObject(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __copy__(self):
        return self.__class__(**self.__dict__)

    def __deepcopy__(self, memo):
        kwargs = {key: _deepcopy(value) for key, value in self.__dict__.items()}
        return self.__class__(**kwargs)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, key))

    @classmethod
    def from_csv(cls, path):
        list_ = _io.csv2list(path)
        headers = {key: _snake_case(key) for key in list_[0]}
        return [cls(**{header: dict_[key] for key, header in headers.items()}) for dict_ in list_]

    @classmethod
    def from_dict(cls, dict_):
        assert isinstance(dict_, dict)
        return cls(**{_snake_case(key): value for key, value in dict_.items()})

    @classmethod
    def from_list(cls, list_):
        assert isinstance(list_, dict)
        return cls(**{"param%s" % index: item for index, item in enumerate(list_)})

    @classmethod
    def from_tsv(cls, path):
        list_ = _io.tsv2list(path)
        headers = {key: _snake_case(key) for key in list_[0]}
        return [cls(**{header: dict_[key] for key, header in headers.items()}) for dict_ in list_]


class ImmutableLazyObject(LazyObject):

    def __setattr__(self, key, value):
        raise AttributeError("can't set attribute '%s' objects are immutable" % type(self).__name__)
