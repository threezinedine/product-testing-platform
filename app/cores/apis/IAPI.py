from abc import ABC, abstractmethod


class IAPI(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
