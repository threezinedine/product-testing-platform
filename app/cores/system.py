from typing import List
from copy import deepcopy
from app.cores.constants import (
    API_KEY,
    ARGS_KEY,
    KWARGS_KEY,
)

from app.cores.interfaces import IApplication
from app.cores.apis import (
    IAPI,
    CreateNewVariableAPI,
    RemoveVariableAPI,
)


class System:
    def __init__(self, applications: List[IApplication] = []) -> None:
        self.__application = applications
        self.__variables = {}

    def runApplication(self, application_name: str) -> None:
        for application in self.__application:
            if application.name == application_name:
                for api in application.apis:
                    self.runAPI(api[API_KEY], *api[ARGS_KEY],
                                **api[KWARGS_KEY])

    def runAPI(self, api_class_name: IAPI, *args, **kwargs) -> None:
        api = globals()[api_class_name]()
        new_variables_dict = api.run(
            *args, variables=deepcopy(self.__variables), **kwargs)

        self.__variables = new_variables_dict

    @property
    def variables(self) -> dict:
        return self.__variables
