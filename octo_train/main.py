import os

from octo_train.db.tinydbdatabase import TinyDBDatabase
from octo_train.menu.menu_interfaces import Menu
from octo_train.menu.menu_states import MainMenuState, WelcomeState


class MainProcess:
    def __init__(self, path_to_database):
        self.db = db = TinyDBDatabase(path_to_database)
        if db.loaded:
            self._state = Menu(db, MainMenuState())
        else:
            self._state = Menu(db, WelcomeState())

    def run(self):
        while True:
            self._state.show()
            self._state.process_input()


def main():
    path_to_database = os.path.expanduser('~/octo_train_data.json')
    main_process = MainProcess(path_to_database)
    main_process.run()


if __name__ == '__main__':
    main()
