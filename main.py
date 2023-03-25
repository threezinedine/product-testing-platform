from app.utils.base import PublisherBase
from app.utils.interfaces import (
    IObserver,
    IPublisher,
)


class ConsoleObserver(IObserver):
    def update(self, publisher: 'IPublisher', data: dict) -> None:
        print(data)


class ConsoleBeautyObserver(IObserver):
    def update(self, publisher: 'IPublisher', data: dict) -> None:
        print('Name changed to: {}'.format(data['name']))


class NameVariablePublisher(PublisherBase):
    def __init__(self):
        super().__init__()
        self._dict['name'] = 'John'

    def set_name(self, name: str) -> None:
        self._dict['name'] = name
        self.notify()


if __name__ == '__main__':
    variable = NameVariablePublisher()
    observer = ConsoleObserver()
    beauty_observer = ConsoleBeautyObserver()
    variable.add_observer(observer)
    variable.add_observer(beauty_observer)

    variable.set_name('John')
    variable.set_name('Jane')

    variable.remove_observer(observer)

    variable.set_name('John')
