from .change_variable_value_api import ChangeVariableValueAPI
from app.cores.constants import ERROR_VARIABLE_NAME
from app.cores.interfaces import (
    IAPI,
    ISystem,
)
from app.cores import Error


class RaiseErrorAPI(IAPI):
    def run(self, errorStr: Error, system: 'ISystem' = None, **kwargs) -> None:
        return ChangeVariableValueAPI().run(
            variable_name=ERROR_VARIABLE_NAME,
            new_value=errorStr.value,
            system=system,
            variables=system.variables,
        )
