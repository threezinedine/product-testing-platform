from copy import deepcopy

from app.utils.interfaces import (
    IPublisher,
    IObserver,
)


class PublisherBase(IPublisher):
    def __init__(self):
        self.__observers = []
        self._dict = {}

    def add_observer(self, observer: 'IObserver') -> int:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer: 'IObserver') -> None:
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self) -> None:
        for observer in self.__observers:
            observer.update(self, deepcopy(self._dict))
