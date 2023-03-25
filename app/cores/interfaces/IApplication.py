import numpy as np
from typing import List
from abc import ABC, abstractproperty, abstractmethod

from app.cores.apis import IAPI


class IApplication(ABC):
    @abstractproperty
    def apis(self) -> List[IAPI]:
        raise NotImplementedError

    @abstractproperty
    def name(self) -> str:
        raise NotImplementedError

    @abstractproperty
    def icon(self) -> np.ndarray:
        raise NotImplementedError
