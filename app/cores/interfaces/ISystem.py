from abc import ABC, abstractmethod, abstractproperty


class ISystem(ABC):
    @abstractproperty
    def variables(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def runAPI(self, api_class_name: str, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def runApplication(self, application_name: str) -> None:
        raise NotImplementedError
