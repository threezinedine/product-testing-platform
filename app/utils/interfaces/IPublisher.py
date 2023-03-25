from abc import ABC, abstractmethod

from app.utils.interfaces import IObserver


class IPublisher(ABC):
    @abstractmethod
    def add_observer(self, observer: 'IObserver') -> int:
        raise NotImplementedError

    @abstractmethod
    def remove_observer(self, observer: 'IObserver') -> None:
        raise NotImplementedError

    @abstractmethod
    def notify(self) -> None:
        raise NotImplementedError
