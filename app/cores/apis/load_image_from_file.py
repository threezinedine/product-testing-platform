import cv2 as cv

from app.cores.apis import CreateNewVariableAPI
from app.cores.constants import EMPTY_DICT
from app.cores.interfaces import (
    IAPI,
    ISystem,
)


class LoadImageFromFileAPI(IAPI):
    def run(self, variable_name: str, file_path: str,
            variables: dict = EMPTY_DICT,
            system: 'ISystem' = None, **kwargs):

        image = cv.imread(file_path)
        return CreateNewVariableAPI().run(
            variable_name=variable_name,
            initial_value=image,
            system=system,
            variables=variables,
        )
