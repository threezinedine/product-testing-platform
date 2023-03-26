import numpy as np
from enum import (
    Enum,
    auto,
)


class VariableType:
    OBJECT = 'object'
    NUMBER = 'number'
    STRING = 'string'
    IMAGE = 'image'

    def get_type_of_value(value: object):
        if isinstance(value, np.ndarray):
            return VariableType.IMAGE
        elif isinstance(value, int) or isinstance(value, float):
            return VariableType.NUMBER
        elif isinstance(value, str) or isinstance(value, VariableType):
            return VariableType.STRING
        else:
            return VariableType.OBJECT
