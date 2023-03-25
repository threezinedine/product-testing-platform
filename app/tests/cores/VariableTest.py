import unittest

from app.cores import (
    Variable,
    VariableType,
)
from app.cores.constants import (
    VALUE_KEY,
)


TEST_VARIABLE_NAME = 'test_variable'
TEST_VARIABLE_NUMBER_VALUE = 1
TEST_VARIABLE_NEW_NUMBER_VALUE = 2
TEST_VARIABLE_STRING_VALUE = 'string'


class VariableTest(unittest.TestCase):
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
        def change_variable_value(data: dict) -> None:
            data[VALUE_KEY] = TEST_VARIABLE_NEW_NUMBER_VALUE
            return data

        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)
        variable.act(change_variable_value)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, TEST_VARIABLE_NEW_NUMBER_VALUE)

    def test_change_value_of_variable_vai_callback_with_different_type(self):
        def change_variable_value(data: dict) -> None:
            data[VALUE_KEY] = TEST_VARIABLE_STRING_VALUE
            return data

        variable = Variable(TEST_VARIABLE_NAME, TEST_VARIABLE_NUMBER_VALUE)
        variable.act(change_variable_value)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, TEST_VARIABLE_NUMBER_VALUE)
        self.assertEqual(variable.type, VariableType.NUMBER)

    def test_with_object_variable_after_acting_new_type_is_assigned(self):
        def change_variable_value(data: dict) -> None:
            data[VALUE_KEY] = TEST_VARIABLE_STRING_VALUE
            return data

        variable = Variable(TEST_VARIABLE_NAME)
        variable.act(change_variable_value)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, TEST_VARIABLE_STRING_VALUE)
        self.assertEqual(variable.type, VariableType.STRING)

    def test_with_variable_after_acting_missing_some_value_or_type(self):
        def chage_variable_value(data: dict) -> None:
            return {VALUE_KEY: 'string'}

        variable = Variable(TEST_VARIABLE_NAME)

        variable.act(chage_variable_value)

        self.assertEqual(variable.name, TEST_VARIABLE_NAME)
        self.assertEqual(variable.value, None)
        self.assertEqual(variable.type, VariableType.OBJECT)
