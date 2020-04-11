from datetime import datetime
from random import randint
from tinydb import TinyDB, where

from octo_train.db.database_interface import IDatabase


class TinyDBDatabase(IDatabase):
    _DATE_FORMAT = '%d.%m.%y'

    def __init__(self, path_to_db):
        self.db = TinyDB(path_to_db)
        self.user = None
        self.loaded = False
        if self.db.contains(where('name')):
            self.loaded = True
            self.user = self._get_user()

    def new_user(self, **kwargs):
        self.db.insert(kwargs)
        self.user = self._get_user()

    def get_stats(self):
        pass

    def solved_today(self, problem_type):
        today = self._get_today_date()
        st = self.db.search((where('date') == today)
                            & (where('problem_type') == problem_type)
                            & (where('solved') == True))
        return len(st)

    def get_solved(self, problem_type):
        l = self.db.search((where('problem_type') == problem_type) & (where('solved') == True))
        result = set()
        for item in l:
            result.add(item['link'])
        return result

    def get_not_solved(self, problem_type):
        l = self.db.search((where('problem_type') == problem_type) & (where('solved') == False))
        result = set()
        for item in l:
            result.add(item['link'])
        return result

    def get_all(self, problem_type):
        l = self.db.search(where('problem_type') == problem_type)
        result = set()
        for item in l:
            result.add(item['link'])
        return result

    def get_not_solved_problem(self, problem_type):
        l = self.db.search((where('problem_type') == problem_type) & (where('solved') == False))
        if not l:
            return None
        problem_number = randint(0, len(l) - 1)
        problem = l[problem_number]
        self.db.remove(where('link') == problem['link'])
        return problem

    def insert(self, problem_data):
        problem_data['date'] = self._get_today_date()
        self.db.insert(problem_data)

    def update_user(self, key, value):
        self.user[key] = value
        self.db.write_back([self.user])

    def _get_user(self):
        try:
            user = self.db.search(where('name'))[0]
        except IndexError:
            raise
        else:
            return user

    def _get_today_date(self):
        return datetime.now().strftime(self._DATE_FORMAT)
