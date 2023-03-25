from app.cores.constants import VALUE_KEY
from app.cores.interfaces import (
    IAPI,
    ISystem,
)


class ChangeVariableValueAPI(IAPI):
    def run(self, variable_name: str, new_value: object,
            system: 'ISystem' = None, variables: dict = {}) -> dict:

        def change_value(data: dict):
            data[VALUE_KEY] = new_value
            return data

        variables[variable_name].act(change_value, system)
        return variables
