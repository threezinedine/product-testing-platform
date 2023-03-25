from typing import List
from copy import deepcopy

from app.cores.interfaces import IApplication
from app.cores.apis import IAPI


class System:
    def __init__(self, applications: List[IApplication] = []) -> None:
        self.__variables = {}

    def runAPI(self, api: IAPI, *args, **kwargs) -> None:
        new_variables_dict = api.run(
            *args, variables=deepcopy(self.__variables), **kwargs)
        
        self.__variables = new_variables_dict

    @property
    def variables(self) -> dict:
        return self.__variables
