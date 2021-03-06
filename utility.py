import os
import re
from typing import Optional, Union

def _parse_number(value: str, type_cls) -> int:
    """
    value starts with 0x is hexadecimal, with 0b is binary,
    with 0 is octal, else it is decimal
    :param value:
    :param type_cls:
    :return:
    """
    if value[:2].lower() == '0x':
        base = 16
    elif value[:2].lower() == '0b':
        base = 2
    elif value[:1] == '0':
        base = 8
    else:
        base = 10

    return type_cls(value, base)


def parse_int(value: Optional[str]):
    return _parse_number(value, int)


def parse_bool(value: Optional[Union[str, bool]]):
    if isinstance(value, bool):
        return value

    if value.lower() == 'true':
        return True
    elif value.lower() == 'yes':
        return True
    elif value.lower() == 'false':
        return False
    elif value.lower() == 'no':
        return False
    else:
        raise Exception('%s: unknown value' % repr(value))


def parse_type(type_str: str):
    if type_str.lower() == 'str':
        return str
    elif type_str.lower() == 'int':
        return int
    elif type_str.lower() == 'bool':
        return bool
    else:
        raise Exception('%s: unknown type string' % repr(type_str))


def contains_characters(string: str, characters: str) -> bool:
    if not string:
        return False

    if not characters:
        return False

    for char in characters:
        if char in string:
            return True
    return False


def list_patterns(path, pattern):
    """
    list files with name matches the pattern under the given path,
    if nothing found or the path not exists, return empty list []

    Caution: we do not care if the found is regular or directory
    :param path:
    :param pattern:
    :return:
    """
    if not os.path.exists(path):
        return []
    if not os.path.isdir(path):
        return []

    filenames = []
    for filename in os.listdir(path):
        if re.match(pattern, filename):
            filenames.append(filename)
    return filenames


def extract_parameter(shell, kwargs_dict, parameter, param_string_in_config):
    if parameter in kwargs_dict:
        return kwargs_dict[parameter]
    else:
        return shell.config[param_string_in_config]