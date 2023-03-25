from app.cores.interfaces import (
    IAPI,
    ISystem,
)


class RemoveVariableAPI(IAPI):
    def run(self, variable_name: str,
            system: 'ISystem' = None,
            variables: dict = {}) -> dict:
        del variables[variable_name]
        return variables
