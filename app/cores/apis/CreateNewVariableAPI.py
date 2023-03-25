from typing import Dict

from app.cores import Variable
from .IAPI import IAPI


class CreateNewVariableAPI(IAPI):
    def run(self, variable_name: str,
            initial_value: object = None,
            variables: dict = {}) -> Dict[str, Variable]:
        variables[variable_name] = Variable(variable_name, initial_value)
        return variables
