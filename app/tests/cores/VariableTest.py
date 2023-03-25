import unittest
from unittest.mock import Mock

from app.cores import (
    Variable,
    VariableType,
    Error,
)
from app.cores.apis.raise_error_api import RaiseErrorAPI
from app.cores.interfaces import ISystem
from app.cores.constants import (
    TYPE_KEY,
    VALUE_KEY,
)


TEST_VARIABLE_NAME = 'test_variable'
TEST_VARIABLE_NUMBER_VALUE = 1
TEST_VARIABLE_NEW_NUMBER_VALUE = 2
TEST_VARIABLE_STRING_VALUE = 'string'


def change_variable_value_number(data: dict) -> None:
    data[VALUE_KEY] = TEST_VARIABLE_NEW_NUMBER_VALUE
    return data


def change_variable_value_string(data: dict) -> None:
    data[VALUE_KEY] = TEST_VARIABLE_STRING_VALUE
    return data


def change_variable_value_miss_type(data: dict) -> None:
    return {VALUE_KEY: TEST_VARIABLE_STRING_VALUE}


def change_variable_value_miss_value(data: dict) -> None:
    return {TYPE_KEY: VariableType.STRING}


class VariableTest(unittest.TestCase):
    def setUp(self):
        self.system = Mock(ISystem)

    def test_variable_name(self):
        variable = Variable(TEST_VARIABLE_NAME)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.type, VariableType.OBJECT)
        self.assertEqual(variable.value, None)

    def test_variable_with_intial_value(self):
        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.type, VariableType.NUMBER)
        self.assertEqual(variable.value, TEST_VARIABLE_NUMBER_VALUE)

    def test_variable_with_string_initial_value(self):
        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_STRING_VALUE)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.type, VariableType.STRING)
        self.assertEqual(variable.value, TEST_VARIABLE_STRING_VALUE)

    def test_change_value_of_variable_via_callback(self):

        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)
        variable.act(change_variable_value_number, self.system)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, TEST_VARIABLE_NEW_NUMBER_VALUE)

    def test_change_value_of_variable_vai_callback_with_different_type(self):
        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)
        variable.act(change_variable_value_string, self.system)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, TEST_VARIABLE_NUMBER_VALUE)
        self.assertEqual(variable.type, VariableType.NUMBER)

    def test_with_object_variable_after_acting_new_type_is_assigned(self):
        variable = Variable(TEST_VARIABLE_NAME)
        variable.act(change_variable_value_string, self.system)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, TEST_VARIABLE_STRING_VALUE)
        self.assertEqual(variable.type, VariableType.STRING)

    def test_with_variable_after_acting_missing_some_value_or_type(self):

        variable = Variable(TEST_VARIABLE_NAME)

        variable.act(change_variable_value_miss_type, self.system)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, None)
        self.assertEqual(variable.type, VariableType.OBJECT)

    def test_if_assign_variable_with_wrong_type_then_raise_error(self):
        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)

        variable.act(change_variable_value_string, self.system)

        self.system.runAPI.assert_called_once_with(
            RaiseErrorAPI.__name__, Error.TYPE_MISS_MATCH)

    def test_if_assign_variable_with_miss_value_then_raise_error(self):
        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)

        variable.act(change_variable_value_miss_value, self.system)

        self.system.runAPI.assert_called_once_with(
            RaiseErrorAPI.__name__, Error.VALUE_IS_NONE)

    def test_if_assign_variable_with_miss_type_then_raise_error(self):
        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)

        variable.act(change_variable_value_miss_type, self.system)

        self.system.runAPI.assert_called_once_with(
            RaiseErrorAPI.__name__, Error.TYPE_IS_NONE)
