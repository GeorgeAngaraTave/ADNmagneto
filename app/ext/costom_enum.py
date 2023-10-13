# -*- coding: utf-8 -*-
from enum import Enum


class CustomEnum(Enum):

    @classmethod
    def to_array(cls):
        return [{'name': a.name, 'value': a.value} for a in cls]

    @classmethod
    def to_dict(cls):
        _result = {}
        for e in cls:
            _result[e.name] = e.value
        return _result

    @classmethod
    def exist_value(cls, _value):
        return cls.get_by_value(_value) is not None

    @classmethod
    def exist_name(cls, _name):
        return cls.get_by_name(_name) is not None

    @classmethod
    def get_by_value(cls, _value):
        try:
            return cls(int(_value))
        except:
            return None

    @classmethod
    def get_by_name(cls, _name):
        try:
            return cls[_name]
        except:
            return None
