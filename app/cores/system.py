from typing import List
from copy import deepcopy
from app.cores.constants import (
    API_KEY,
    ARGS_KEY,
    EMPTY_STRING,
    ERROR_VARIABLE_NAME,
    KWARGS_KEY,
    EMPTY_LIST,
)

from app.cores.interfaces import IApplication
from app.cores.variable import Variable
from app.cores.apis import *


class System:
    def __init__(self, applications: List['IApplication'] = EMPTY_LIST) -> None:
        self.__application = applications
        self.__variables = {
            ERROR_VARIABLE_NAME: Variable(ERROR_VARIABLE_NAME, EMPTY_STRING),
        }

    def runApplication(self, application_name: str) -> None:
        for application in self.__application:
            if application.name == application_name:
                for api in application.apis:
                    self.runAPI(api[API_KEY], *api[ARGS_KEY],
                                **api[KWARGS_KEY])

    def runAPI(self, api_class_name: str, *args, **kwargs) -> None:
        api = globals()[api_class_name]()
        new_variables_dict = api.run(
            *args, variables=deepcopy(self.__variables),
            system=self, **kwargs)

        self.__variables = new_variables_dict

    @property
    def variables(self) -> dict:
        return self.__variables
