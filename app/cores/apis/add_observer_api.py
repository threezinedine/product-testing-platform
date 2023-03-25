from typing import List

from app.cores.constants import EMPTY_DICT, EMPTY_LIST
from app.cores.interfaces import (
    IAPI,
    ISystem,
)
from app.utils.interfaces import IObserver


class AddObserverAPI(IAPI):
    def run(self, variables_name: str, observer: 'IObserver',
            system: 'ISystem' = None, variables: dict = EMPTY_DICT):
        variables[variables_name].add_observer(observer)
        return variables
