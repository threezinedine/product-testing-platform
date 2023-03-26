from typing import Dict, List

from app.cores.interfaces import ISystem
from app.utils.interfaces import (
    IObserver,
    IPublisher,
)


class APIObserver(IObserver):
    def __init__(self, api_name: str,
                 args: List[object],
                 kwargs: Dict[str, object],
                 system: 'ISystem'):
        self.__api_name = api_name
        self.__args = args
        self.__kwargs = kwargs
        self.system = system

    def update(self, publisher: 'IPublisher', data: dict) -> None:
        self.system.runAPI(self.__api_name, *self.__args, **self.__kwargs)
