from abc import ABC, abstractmethod
from octo_train.db.tinydbdatabase import TinyDBDatabase


class IProblem(ABC):
    def __init__(self, title, difficulty, link):
        self.title = title
        self.difficulty = difficulty
        self.link = link
        self.solved = False

    @abstractmethod
    def json(self):
        return {
            'title': self.title,
            'difficulty': self.difficulty,
            'link': self.link,
            'solved': self.solved
        }


class IProblemSource(ABC):
    def __init__(self, db: TinyDBDatabase):
        self.db = db

    def add_problem_to_db(self, task):
        self.db.insert(task.json())

    @abstractmethod
    def get_problem(self):
        pass

    @abstractmethod
    def solved_today(self):
        pass

    @abstractmethod
    def goal(self):
        pass
