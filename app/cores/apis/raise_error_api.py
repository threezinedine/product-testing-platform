from typing import List
from .change_variable_value_api import ChangeVariableValueAPI
from app.cores.constants import EMPTY_LIST, ERROR_VARIABLE_NAME
from app.cores.interfaces import (
    IAPI,
    ISystem,
)
from app.cores import Error


class RaiseErrorAPI(IAPI):
    def run(self, errorStr: Error,
            system: 'ISystem' = None,
            variables: List[object] = EMPTY_LIST,
            **kwargs) -> None:
        system.raiseError(errorStr)
        return variables
