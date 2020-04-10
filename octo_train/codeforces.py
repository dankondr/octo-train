import requests
from bs4 import BeautifulSoup
from random import randint

from octo_train.source_interface import Problem, ProblemSource

BASE_URL = 'https://codeforces.com'


class CFProblem(Problem):
    def json(self):
        d = super().json()
        d['problem_type'] = 'cf'
        return d


class CodeForces(ProblemSource):
    def get_problem(self):
        give_not_solved = randint(1, 100) <= 33
        if give_not_solved:
            problem = self.db.get_not_solved_problem('cf')
            if problem is not None:
                return CFProblem(problem['title'], problem['difficulty'], problem['link'])

        difficulty = int(self.db.user['cf_level'])
        solved = self.db.get_all('cf')
        start_page = self.db.user['cf_page']
        for i in range(start_page, 61):
            url = f'{BASE_URL}/problemset/page/{i}?order=BY_RATING_ASC'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            problems = soup.find('table', 'problems')('tr')
            for problem in problems:
                difficulty_cell = problem.select('td > span.ProblemRating')
                if not difficulty_cell:
                    continue
                problem_difficulty = int(difficulty_cell[0].text)
                if problem_difficulty < difficulty:
                    continue
                title_cell = problem.select('td > div > a')
                if not title_cell:
                    continue
                title_cell = title_cell[0]
                link = BASE_URL + title_cell['href']
                if link in solved:
                    continue
                title = title_cell.text.replace('\n', '').rstrip(' ')

                if i > start_page:
                    self.db.update_user('cf_page', i)

                if problem_difficulty > difficulty:
                    self.db.update_user('cf_level', problem_difficulty)

                return CFProblem(title, problem_difficulty, link)

    def solved_today(self):
        return int(self.db.solved_today('cf'))

    def goal(self):
        return int(self.db.user['cf_daily'])
