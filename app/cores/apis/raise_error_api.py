from .change_variable_value_api import ChangeVariableValueAPI
from app.cores.constants import ERROR_VARIABLE_NAME
from app.cores.interfaces import (
    IAPI,
    ISystem,
)


class RaiseErrorAPI(IAPI):
    def run(self, errorStr: str, system: 'ISystem' = None, **kwargs) -> None:
        api = ChangeVariableValueAPI()
        return api.run(
            variable_name=ERROR_VARIABLE_NAME,
            new_value=errorStr,
            system=system,
            variables=system.variables,
        )
