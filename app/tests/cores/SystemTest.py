import unittest
import numpy as np

from app.cores import System
from app.cores.interfaces import IApplication
from app.cores.apis import (
    CreateNewVariableAPI,
    RemoveVariableAPI,
)


TEST_VARIABLE_NAME = 'test_variable'
TEST_VARIABLE_INTIAL_VALUE = 1


class TestApplication(IApplication):
    def run(self):
        pass

    def stop(self):
        pass

    def getName(self):
        return 'TestApplication'

    def getIcon(self) -> np.ndarray:
        return np.zeros((1, 1, 3), dtype=np.uint8)


class SystemTest(unittest.TestCase):
    def setUp(self):
        self.applications = [
            TestApplication(),
        ]
        self.system = System(self.applications)

    def create_new_variable(self):
        self.system.runAPI(CreateNewVariableAPI(),
                           TEST_VARIABLE_NAME,
                           initial_value=TEST_VARIABLE_INTIAL_VALUE)

    def test_system_initialization(self):
        system = System(self.applications)

    def test_system_run_create_new_variable_API(self):
        self.system.runAPI(CreateNewVariableAPI(),
                           TEST_VARIABLE_NAME,
                           initial_value=TEST_VARIABLE_INTIAL_VALUE)

        self.system.variables[TEST_VARIABLE_NAME].value == TEST_VARIABLE_INTIAL_VALUE

    def test_system_runs_remove_variable_API(self):
        self.create_new_variable()
        self.system.runAPI(RemoveVariableAPI(),
                           TEST_VARIABLE_NAME)

        self.assertNotIn(TEST_VARIABLE_NAME, self.system.variables.keys())
