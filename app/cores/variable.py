from copy import deepcopy

from app.cores.constants import (
    TYPE_KEY,
    VALUE_KEY,
)
from app.cores.variable_type import VariableType
from app.cores.interfaces import ISystem
from app.cores import Error
from app.utils.base import PublisherBase
from app.utils.interfaces import (
    IObserver,
)


class Variable(PublisherBase):
    def __init__(self, name: str, value: object = None):
        super().__init__()
        self.__name = name
        self._dict[VALUE_KEY] = value
        self._dict[TYPE_KEY] = VariableType.get_type_of_value(value)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> str:
        return self._dict[TYPE_KEY]

    @property
    def value(self) -> object:
        return self._dict[VALUE_KEY]

    def act(self, func, system: 'ISystem') -> None:
        new_dict = func(deepcopy(self._dict))

        if VALUE_KEY not in new_dict.keys():
            system.runAPI('RaiseErrorAPI',
                          Error.VALUE_IS_NONE)
            return
        elif TYPE_KEY not in new_dict.keys():
            system.runAPI('RaiseErrorAPI',
                          Error.TYPE_IS_NONE)
            return

        if self.type == VariableType.OBJECT:
            new_dict[TYPE_KEY] = VariableType.get_type_of_value(
                new_dict[VALUE_KEY])
            self._dict = new_dict
        elif VariableType.get_type_of_value(new_dict[VALUE_KEY]) == self.type:
            self._dict = new_dict
        else:
            system.runAPI('RaiseErrorAPI',
                          Error.TYPE_MISS_MATCH)

        self.notify()
