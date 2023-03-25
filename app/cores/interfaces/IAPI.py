from abc import ABC, abstractmethod
from typing import List


from app.cores.constants import EMPTY_DICT
from app.cores.interfaces import ISystem


class IAPI(ABC):
    @abstractmethod
    def run(self, *args, system: 'ISystem' = None,
            variables: dict = EMPTY_DICT, **kwargs):
        raise NotImplementedError
