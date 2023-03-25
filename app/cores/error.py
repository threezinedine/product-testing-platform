from enum import Enum


class Error(Enum):
    TYPE_MISS_MATCH = 'New value type does not match.'
    VALUE_IS_NONE = 'New value is None.'
    TYPE_IS_NONE = 'New type is None.'
