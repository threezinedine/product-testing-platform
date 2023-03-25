import numpy as np
from typing import List
from app.cores.constants import (
    API_KEY,
    ARGS_KEY,
    EMPTY_DICT,
    KWARGS_KEY,
)
from app.cores import System
from app.utils.base import PublisherBase
from app.utils.interfaces import (
    IObserver,
    IPublisher,
)
from app.cores.interfaces import (
    IAPI,
    IApplication,
)


class Application(IApplication):
    @property
    def name(self) -> str:
        return 'Application'

    @property
    def icon(self) -> np.ndarray:
        return np.zeros((10, 10, 3), dtype=np.uint8)

    @property
    def apis(self) -> List['IAPI']:
        return [
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: [
                    'test_variable',
                ],
                KWARGS_KEY: dict(
                    initial_value=1,
                ),
            },
            {
                API_KEY: 'ChangeVariableValueAPI',
                ARGS_KEY: [
                    'test_variable',
                    'string',
                ],
                KWARGS_KEY: EMPTY_DICT,
            },
        ]


if __name__ == '__main__':
    system = System([Application()])
    system.runApplication('Application')
