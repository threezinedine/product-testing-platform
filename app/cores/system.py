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
        self.__applications = {
            application.name: application
            for application in applications
        }
        self.__error = Variable(ERROR_VARIABLE_NAME, EMPTY_STRING)
        self.__variables = EMPTY_DICT

    def runApplication(self, application_name: str) -> None:
        if application_name not in self.__applications.keys():
            self.runAPI('RaiseErrorAPI', Error.APPLICATION_NOT_FOUND)
            return

        for api in self.__applications[application_name].apis:
            self.runAPI(api[API_KEY], *api[ARGS_KEY],
                        **api[KWARGS_KEY])

    def runAPI(self, api_class_name: str, *args, **kwargs) -> None:
        api = globals()[api_class_name]()

        new_variables_dict = api.run(
            *args,
            variables=self.__get_copy_variables(),
            system=self, **kwargs)

        self.__variables = new_variables_dict

    def __get_copy_variables(self) -> dict:
        return {
            variable_name: variable
            for variable_name, variable in self.__variables.items()
        }

    def raiseError(self, error: Error) -> None:
        def raiseErrorFunc(data: dict):
            data[VALUE_KEY] = error.value
            return data

        self.__error.act(raiseErrorFunc, self)

    @property
    def variables(self) -> dict:
        variables = deepcopy(self.__variables)
        variables[ERROR_VARIABLE_NAME] = self.__error
        return variables
