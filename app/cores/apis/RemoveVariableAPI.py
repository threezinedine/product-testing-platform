from .IAPI import IAPI


class RemoveVariableAPI(IAPI):
    def run(self, variable_name: str, variables: dict = {}) -> dict:
        del variables[variable_name]
        return variables
