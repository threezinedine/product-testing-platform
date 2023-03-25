import unittest
from unittest.mock import Mock

from app.utils.base import (
    PublisherBase,
)
from app.utils.interfaces import (
    IObserver,
    IPublisher,
)


NAME_KEY = 'name'
TEST_NAME = 'John'
TEST_CHANGED_NAME = 'Jane'


class TestPublisher(PublisherBase):
    def __init__(self):
        super().__init__()
        self._dict[NAME_KEY] = TEST_NAME

    def get_dict(self) -> dict:
        return self._dict


class ChangeNameObserver(IObserver):
    def update(self, publisher: 'IPublisher', data: dict) -> None:
        data[NAME_KEY] = TEST_CHANGED_NAME


class PublisherBaseTest(unittest.TestCase):
    def setUp(self):
        self.publisher = TestPublisher()
        self.expected_return_dict = {
            NAME_KEY: TEST_NAME
        }

        self.first_observer = Mock(spec=IObserver)
        self.second_observer = Mock(spec=IObserver)
        self.third_observer = Mock(spec=IObserver)

    def test_invoke_all_observers_when_notify(self):
        self.publisher.add_observer(self.first_observer)
        self.publisher.add_observer(self.second_observer)

        self.publisher.notify()

        self.first_observer.update.assert_called_once_with(self.publisher,
                                                           self.expected_return_dict)
        self.second_observer.update.assert_called_once_with(self.publisher,
                                                            self.expected_return_dict)
        self.third_observer.update.assert_not_called()

    def test_removed_observer_will_not_be_invoked(self):
        self.publisher.add_observer(self.first_observer)
        self.publisher.add_observer(self.second_observer)

        self.publisher.notify()

        self.publisher.remove_observer(self.second_observer)

        self.publisher.notify()

        self.first_observer.update.assert_called_with(self.publisher,
                                                      self.expected_return_dict)
        self.assertEqual(self.first_observer.update.call_count, 2)
        self.second_observer.update.assert_called_once_with(self.publisher,
                                                            self.expected_return_dict)

    def test_the_dict_which_the_observer_received_is_a_copy(self):
        self.publisher.add_observer(ChangeNameObserver())

        self.publisher.notify()

        self.assertEqual(self.publisher.get_dict()[NAME_KEY], TEST_NAME)

    def test_remove_non_existed_nothing_happen(self):
        self.publisher.add_observer(self.first_observer)

        self.publisher.remove_observer(self.second_observer)

        self.publisher.notify()

        self.first_observer.update.assert_called_once_with(self.publisher,
                                                           self.expected_return_dict)
        self.second_observer.update.assert_not_called()

    def test_add_existed_observer_that_observer_will_not_be_invoked_twice(self):
        self.publisher.add_observer(self.first_observer)
        self.publisher.add_observer(self.first_observer)

        self.publisher.notify()

        self.first_observer.update.assert_called_once_with(self.publisher,
                                                           self.expected_return_dict)
