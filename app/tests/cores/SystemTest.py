import unittest
import numpy as np
from typing import List

from app.cores import System
from app.cores.constants import (
    API_KEY,
    ARGS_KEY,
    ERROR_VARIABLE_NAME,
    KWARGS_KEY,
)
from app.cores.interfaces import IApplication
from app.cores.apis import (
    ChangeVariableValueAPI,
    CreateNewVariableAPI,
    RaiseErrorAPI,
    RemoveVariableAPI,
)
from app.cores.apis import IAPI


TEST_VARIABLE_NAME = 'test_variable'
TEST_VARIABLE_INTIAL_VALUE = 1
TEST_VARIABLE_NEW_VALUE = 2

TEST_VARIABLE_STRING_NAME = 'test_variable_string'
TEST_VARIABLE_STRING_INTIAL_VALUE = 'test'

TEST_APPLICATION_NAME = 'TestApplication'

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


class SystemTest(unittest.TestCase):
    def setUp(self):
        self.applications = [
            TestApplication(),
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
        self.system.runAPI(RaiseErrorAPI.__name__, TEST_ERROR_STRING)

        print(self.system.variables)
        self.system.variables[ERROR_VARIABLE_NAME].value == TEST_ERROR_STRING

    def test_change_value_value(self):
        self.create_new_variable()

        self.system.runAPI(ChangeVariableValueAPI.__name__,
                           TEST_VARIABLE_NAME, TEST_VARIABLE_NEW_VALUE)

        self.system.variables[TEST_VARIABLE_NAME].value == TEST_VARIABLE_NEW_VALUE
