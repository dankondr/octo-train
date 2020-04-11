import os
from abc import ABC, abstractmethod

from octo_train.colored import welcome_message, logo, multisolve
from octo_train.sources.codeforces import CodeForces
from octo_train.sources.euler import ProjectEuler


class Menu(ABC):
    _state = None

    def __init__(self, db, state) -> None:
        self.db = db
        self.cf = CodeForces(db)
        self.pe = ProjectEuler(db)
        self.transition_to(state)

    def transition_to(self, state):
        self._state = state
        self._state.menu = self

    def show(self):
        self._state.show()

    def process_input(self):
        self._state.process_input()


class IMenuState(ABC):
    menu = None

    @abstractmethod
    def show(self):
        self._clear()
        print(logo)

    @abstractmethod
    def process_input(self):
        pass

    def _clear(self):
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
