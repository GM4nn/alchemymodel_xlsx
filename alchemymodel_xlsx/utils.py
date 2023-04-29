# lib
from datetime import datetime
import numpy

DEFAULT_BOOL_VALUES = {True: "Yes", False: "No"}


def datetime_to_str(value: datetime):
    str_date = value.strftime("%Y-%m-%d")
    return str_date


def bool_to_str(value: bool):
    return DEFAULT_BOOL_VALUES[value]


def none_to_str(value):
    return ""


def serialize_value(value):
    types = [str, datetime, int, float, bool, None]

    proccess_types = {
        datetime: datetime_to_str,
        bool: bool_to_str,
        None: none_to_str,
    }

    value_type = type(value)

    if isinstance(value, numpy.generic):
        if value.item() in proccess_types:
            value = proccess_types[value.item()](value)
            return value

    for python_type in types:
        if python_type == value_type:
            if value_type in proccess_types:
                value = proccess_types[value_type](value)
                return value

    return str(value)
