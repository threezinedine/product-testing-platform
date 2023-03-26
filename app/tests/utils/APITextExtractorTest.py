import unittest

from app.cores.constants import (
    API_KEY,
    ARGS_KEY,
    EMPTY_DICT,
    KWARGS_KEY,
    EMPTY_LIST,
)
from app.utils.tools import APITextExtractor


class APITextExtractorTest(unittest.TestCase):
    def test_extract_api_with_name_only(self):
        extractor = APITextExtractor('CreateNewVariableAPI')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: EMPTY_LIST,
                KWARGS_KEY: EMPTY_DICT,
            }
        )

    def test_extract_api_with_one_argument(self):
        extractor = APITextExtractor('CreateNewVariableAPI test_variable')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: ['test_variable'],
                KWARGS_KEY: EMPTY_DICT,
            }
        )

    def test_extract_with_kwargs(self):
        extractor = APITextExtractor(
            'CreateNewVariableAPI test_variable -initial_value string')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: ['test_variable'],
                KWARGS_KEY: {
                    'initial_value': 'string',
                }
            }
        )

    def test_extract_mutilple_args(self):
        extractor = APITextExtractor(
            'ChangeVariableValueAPI test_variable 45'
        )

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'ChangeVariableValueAPI',
                ARGS_KEY: ['test_variable', 45],
                KWARGS_KEY: EMPTY_DICT,
            }
        )

    def test_extract_multiple_args_and_kwargs(self):
        extractor = APITextExtractor(
            'ChangeVariableValueAPI test_variable 45 -test_value 46 -test 1'
        )

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'ChangeVariableValueAPI',
                ARGS_KEY: ['test_variable', 45],
                KWARGS_KEY: {
                    'test_value': 46,
                    'test': 1,
                }
            }
        )

    def test_extract_api_multiple_lines(self):
        extractor = APITextExtractor(
            'CreateNewVariableAPI test_variable\nCreateNewVariableAPI test_variable2')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: ['test_variable'],
                KWARGS_KEY: EMPTY_DICT,
            }
        )

        self.assertDictEqual(
            apis[1],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: ['test_variable2'],
                KWARGS_KEY: EMPTY_DICT,
            }
        )

    def test_extract_api_with_kwargs_with_no_value(self):
        extractor = APITextExtractor(
            'CreateNewVariableAPI test_variable -test_value')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: ['test_variable'],
                KWARGS_KEY: {
                    'test_value': None,
                }
            }
        )

    def test_extract_api_with_multiple_kwargs_and_no_value(self):
        extractor = APITextExtractor(
            'CreateNewVariableAPI -test_value -test')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: EMPTY_LIST,
                KWARGS_KEY: {
                    'test_value': None,
                    'test': None,
                }
            }
        )

    def test_extract_api_with_true_or_false_then_the_value_should_be_True_or_False(self):
        extractor = APITextExtractor(
            'CreateNewVariableAPI true -test False')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: [True],
                KWARGS_KEY: {
                    'test': False,
                }
            }
        )

    def test_extract_api_with_number(self):
        extractor = APITextExtractor(
            'CreateNewVariableAPI 1 -test 2.23')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: [1],
                KWARGS_KEY: {
                    'test': 2.23,
                }
            }
        )

    def test_extract_api_with_negative_float(self):
        extractor = APITextExtractor(
            'CreateNewVariableAPI 1 -test -2.23')

        apis = extractor.apis

        self.assertDictEqual(
            apis[0],
            {
                API_KEY: 'CreateNewVariableAPI',
                ARGS_KEY: [1],
                KWARGS_KEY: {
                    'test': -2.23,
                }
            }
        )

        apis = extractor.apis
