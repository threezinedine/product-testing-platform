import unittest
import numpy as np
from typing import List

from app.cores import System, Error
from app.cores.constants import (
    API_KEY,
    ARGS_KEY,
    EMPTY_DICT,
    ERROR_VARIABLE_NAME,
    KWARGS_KEY,
)
from app.cores.interfaces import IApplication
from app.cores.apis import (
    LoadImageFromFileAPI,
    AddObserverAPI,
    ChangeVariableValueAPI,
    CreateNewVariableAPI,
    RaiseErrorAPI,
    RemoveVariableAPI,
)
from app.cores.apis import IAPI
from app.cores.variable_type import VariableType
from app.utils.interfaces import IObserver


TEST_VARIABLE_NAME = 'test_variable'
TEST_VARIABLE_INTIAL_VALUE = 1
TEST_VARIABLE_NEW_VALUE = 2

TEST_VARIABLE_STRING_NAME = 'test_variable_string'
TEST_VARIABLE_STRING_INTIAL_VALUE = 'test'

TEST_APPLICATION_NAME = 'TestApplication'
TEST_ERROR_APPLICATION_NAME = 'TestErrorApplication'
TEST_NON_EXISTED_APPLICATION_NAME = 'TestNonExistedApplication'

TEST_ERROR_STRING = 'test_error string'

TEST_IMAGE_FILE_PATH = 'app/tests/assets/flow-chart.png'
TEST_IMAGE_VARIABLE_NAME = 'test_image_variable'


class TestApplication(IApplication):
    @property
    def apis(self) -> List[IAPI]:
        return [
            {
                API_KEY: CreateNewVariableAPI.__name__,
                ARGS_KEY: [TEST_VARIABLE_NAME],
                KWARGS_KEY: dict(
                    initial_value=TEST_VARIABLE_INTIAL_VALUE,
                ),
            },
            {
                API_KEY: CreateNewVariableAPI.__name__,
                ARGS_KEY: [TEST_VARIABLE_STRING_NAME],
                KWARGS_KEY: dict(
                    initial_value=TEST_VARIABLE_STRING_INTIAL_VALUE,
                ),
            },
            {
                API_KEY: RemoveVariableAPI.__name__,
                ARGS_KEY: [TEST_VARIABLE_NAME],
                KWARGS_KEY: {},
            },
        ]

    @property
    def name(self) -> str:
        return TEST_APPLICATION_NAME

    @property
    def icon(self) -> np.ndarray:
        return np.zeros((1, 1, 3), dtype=np.uint8)


class TestErrorApplication(TestApplication):
    @property
    def apis(self) -> List[IAPI]:
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

    @property
    def name(self) -> str:
        return TEST_ERROR_APPLICATION_NAME


class ObserverTest(IObserver):
    def __init__(self, value: str):
        self.__value = value
        self.value_changed = False

    def update(self, publisher, data):
        self.value_changed = publisher.value == self.__value
        print("Updated: ", self.value_changed)


class SystemTest(unittest.TestCase):
    def setUp(self):
        self.applications = [
            TestApplication(),
            TestErrorApplication(),
        ]
        self.system = System(self.applications)

    def create_new_variable(self):
        self.system.runAPI(CreateNewVariableAPI.__name__,
                           TEST_VARIABLE_NAME,
                           initial_value=TEST_VARIABLE_INTIAL_VALUE)

    def test_system_initialization(self):
        system = System(self.applications)

    def test_system_run_create_new_variable_API(self):
        self.system.runAPI(CreateNewVariableAPI.__name__,
                           TEST_VARIABLE_NAME,
                           initial_value=TEST_VARIABLE_INTIAL_VALUE)

        self.system.variables[TEST_VARIABLE_NAME].value == TEST_VARIABLE_INTIAL_VALUE

    def test_system_run_create_new_variable_API_with_existed_variable(self):
        self.create_new_variable()

        self.system.runAPI(CreateNewVariableAPI.__name__,
                           TEST_VARIABLE_NAME,
                           initial_value=TEST_VARIABLE_NEW_VALUE)

        self.assertEqual(self.system.variables[ERROR_VARIABLE_NAME].value,
                         Error.VARIABLE_ALREADY_EXISTS.value)

    def test_system_runs_remove_variable_API(self):
        self.create_new_variable()
        self.system.runAPI(RemoveVariableAPI.__name__,
                           TEST_VARIABLE_NAME)

        self.assertNotIn(TEST_VARIABLE_NAME, self.system.variables.keys())

    def test_syste_runs_remove_non_existed_variable_API(self):
        self.system.runAPI(RemoveVariableAPI.__name__,
                           TEST_VARIABLE_NAME)

        self.assertEqual(self.system.variables[ERROR_VARIABLE_NAME].value,
                         Error.VARIABLE_NOT_FOUND.value)

    def test_system_runs_application(self):
        self.system.runApplication(TEST_APPLICATION_NAME)

        self.assertEqual(
            self.system.variables[TEST_VARIABLE_STRING_NAME].value,
            TEST_VARIABLE_STRING_INTIAL_VALUE)

    def test_system_runs_non_existed_application(self):
        self.system.runApplication(TEST_NON_EXISTED_APPLICATION_NAME)

        self.assertEqual(self.system.variables[ERROR_VARIABLE_NAME].value,
                         Error.APPLICATION_NOT_FOUND.value)

    def test_system_raise_error(self):
        self.system.runAPI(RaiseErrorAPI.__name__, Error.TYPE_MISS_MATCH)

        self.assertEqual(
            self.system.variables[ERROR_VARIABLE_NAME].value, Error.TYPE_MISS_MATCH.value)

    def test_change_value_value(self):
        self.create_new_variable()

        self.system.runAPI(ChangeVariableValueAPI.__name__,
                           TEST_VARIABLE_NAME, TEST_VARIABLE_NEW_VALUE)

        self.assertEqual(
            self.system.variables[TEST_VARIABLE_NAME].value, TEST_VARIABLE_NEW_VALUE)

    def test_change_value_value_with_wrong_type(self):
        self.create_new_variable()

        self.system.runAPI(ChangeVariableValueAPI.__name__,
                           TEST_VARIABLE_NAME, TEST_VARIABLE_STRING_INTIAL_VALUE)

        self.assertEqual(
            self.system.variables[ERROR_VARIABLE_NAME].value, Error.TYPE_MISS_MATCH.value)

        self.assertEqual(
            self.system.variables[TEST_VARIABLE_NAME].value, TEST_VARIABLE_INTIAL_VALUE)

    def test_stop_application_when_error_occurs(self):
        self.system.runApplication(TEST_ERROR_APPLICATION_NAME)

        self.assertEqual(
            self.system.variables[ERROR_VARIABLE_NAME].value, Error.TYPE_MISS_MATCH.value)

    def test_assign_observer_for_variable(self):
        self.create_new_variable()
        observer = ObserverTest(TEST_VARIABLE_NEW_VALUE)
        print(observer)

        self.system.runAPI(AddObserverAPI.__name__,
                           TEST_VARIABLE_NAME, observer)

        self.system.runAPI(ChangeVariableValueAPI.__name__,
                           TEST_VARIABLE_NAME, TEST_VARIABLE_NEW_VALUE)

        self.assertTrue(observer.value_changed)

    def test_load_image_variable_from_a_file(self):
        self.system.runAPI(LoadImageFromFileAPI.__name__,
                           TEST_IMAGE_VARIABLE_NAME, TEST_IMAGE_FILE_PATH)

        assert self.system.variables[TEST_IMAGE_VARIABLE_NAME].type == VariableType.IMAGE
