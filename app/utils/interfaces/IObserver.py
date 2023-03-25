from abc import ABC, abstractmethod

from app.utils.interfaces import IPublisher


class IObserver(ABC):
    @abstractmethod
    def update(self, publisher: 'IPublisher', data: dict) -> None:
        pass
