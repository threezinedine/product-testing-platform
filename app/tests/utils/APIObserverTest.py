import unittest
from unittest.mock import Mock

from app.cores.interfaces import ISystem
from app.utils.base import PublisherBase
from app.utils.tools import APIObserver


API_NAME = 'test_api_name'
API_ARGS = []
API_KWARGS = {}


class APIObserverTest(unittest.TestCase):
    def test_the_api_should_be_called_when_the_publisher_notify(self):
        system = Mock(spec=ISystem)
        system.runAPI = Mock()
        observerAPI = APIObserver(API_NAME, API_ARGS,
                                  API_KWARGS, system)

        publisher = PublisherBase()
        publisher.add_observer(observerAPI)

        publisher.notify()
        publisher.notify()

        system.runAPI.assert_called_with(
            API_NAME, *API_ARGS, **API_KWARGS)

        self.assertEqual(system.runAPI.call_count, 2)
