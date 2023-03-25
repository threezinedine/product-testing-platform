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
    AddObserverAPI,
    ChangeVariableValueAPI,
    CreateNewVariableAPI,
    RaiseErrorAPI,
    RemoveVariableAPI,
)
from app.cores.apis import IAPI
from app.utils.interfaces import IObserver


TEST_VARIABLE_NAME = 'test_variable'
TEST_VARIABLE_INTIAL_VALUE = 1
TEST_VARIABLE_NEW_VALUE = 2

TEST_VARIABLE_STRING_NAME = 'test_variable_string'
TEST_VARIABLE_STRING_INTIAL_VALUE = 'test'

TEST_APPLICATION_NAME = 'TestApplication'
TEST_ERROR_APPLICATION_NAME = 'TestErrorApplication'

TEST_ERROR_STRING = 'test_error string'


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
                    initial_value=TEST_VARIABLE_INTIAL_VALUE,
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
        print("Here", publisher.value, self.__value)
        self.value_changed = publisher.value == self.__value


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

    def test_system_runs_remove_variable_API(self):
        self.create_new_variable()
        self.system.runAPI(RemoveVariableAPI.__name__,
                           TEST_VARIABLE_NAME)

        self.assertNotIn(TEST_VARIABLE_NAME, self.system.variables.keys())

    def test_system_runs_application(self):
        self.system.runApplication(TEST_APPLICATION_NAME)

        self.system.variables[TEST_VARIABLE_STRING_NAME].value == TEST_VARIABLE_STRING_INTIAL_VALUE

    def test_system_raise_error(self):
        self.system.runAPI(RaiseErrorAPI.__name__, Error.TYPE_MISS_MATCH)

        self.system.variables[ERROR_VARIABLE_NAME].value == Error.TYPE_MISS_MATCH.value

    def test_change_value_value(self):
        self.create_new_variable()

        self.system.runAPI(ChangeVariableValueAPI.__name__,
                           TEST_VARIABLE_NAME, TEST_VARIABLE_NEW_VALUE)

        self.system.variables[TEST_VARIABLE_NAME].value == TEST_VARIABLE_NEW_VALUE

    def test_stop_application_when_error_occurs(self):
        self.system.runApplication(TEST_ERROR_APPLICATION_NAME)

        self.system.variables[ERROR_VARIABLE_NAME].value == Error.TYPE_MISS_MATCH

    def test_assign_observer_for_variable(self):
        self.create_new_variable()
        observer = ObserverTest(Error.TYPE_MISS_MATCH.value)

        self.system.runAPI(AddObserverAPI.__name__,
                           ERROR_VARIABLE_NAME, observer)

        self.system.runAPI(ChangeVariableValueAPI.__name__,
                           TEST_VARIABLE_NAME, TEST_VARIABLE_STRING_INTIAL_VALUE)

        self.assertTrue(observer.value_changed)
