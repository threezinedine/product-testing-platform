from typing import Dict

from app.cores import Variable

from app.cores import Error
from app.cores.interfaces import (
    IAPI,
    ISystem,
)

from .raise_error_api import RaiseErrorAPI


class CreateNewVariableAPI(IAPI):
    def run(self, variable_name: str,
            initial_value: object = None,
            system: 'ISystem' = None,
            variables: dict = {}) -> Dict[str, 'Variable']:
        if variable_name in variables.keys():
            return RaiseErrorAPI().run(
                Error.VARIABLE_ALREADY_EXISTS,
                system=system, variables=variables)
        else:
            variables[variable_name] = Variable(variable_name, initial_value)
            return variables
