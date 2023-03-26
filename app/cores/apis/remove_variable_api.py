from app.cores.interfaces import (
    IAPI,
    ISystem,
)
from app.cores import Error

from .raise_error_api import RaiseErrorAPI


class RemoveVariableAPI(IAPI):
    def run(self, variable_name: str,
            system: 'ISystem' = None,
            variables: dict = {}) -> dict:

        if variable_name not in variables.keys():
            return RaiseErrorAPI().run(
                Error.VARIABLE_NOT_FOUND,
                system=system, variables=variables)
        else:
            del variables[variable_name]
            return variables
