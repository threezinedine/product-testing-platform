from enum import (
    Enum,
    auto,
)


class VariableType:
    OBJECT = 'object'
    NUMBER = 'number'
    STRING = 'string'

    def get_type_of_value(value: object):
        if isinstance(value, int) or isinstance(value, float):
            return VariableType.NUMBER
        elif isinstance(value, str):
            return VariableType.STRING
        else:
            return VariableType.OBJECT
