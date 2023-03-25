from abc import ABC, abstractmethod


class IApplication(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
