import requests
from bs4 import BeautifulSoup
from random import randint

from octo_train.source_interface import Problem, ProblemSource

BASE_URL = 'https://projecteuler.net'


class PEProblem(Problem):
    def json(self):
        d = super().json()
        d['problem_type'] = 'pe'
        return d


class ProjectEuler(ProblemSource):
    def get_problem(self):
        give_not_solved = randint(1, 100) <= 33
        if give_not_solved:
            problem = self.db.get_not_solved_problem('pe')
            if problem is not None:
                return PEProblem(problem['title'], problem['difficulty'], problem['link'])

        difficulty = self.db.user['pe_level']
        solved = self.db.get_all('pe')

    def solved_today(self):
        return int(self.db.solved_today('pe'))

    def goal(self):
        return int(self.db.user['pe_daily'])
