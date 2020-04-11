import sys

from octo_train.menu.menu_interfaces import IMenuState
from octo_train.colored import multisolve, welcome_message


class CodeForcesState(IMenuState):
    problem = None

    def show(self):
        super().show()
        self.problem = problem = self.menu.cf.get_problem()
        print(problem.title, f'({problem.difficulty})')
        print(problem.link)

    def process_input(self):
        inp_to_process = input('Solved? (y/n): ')
        solved = self._input_to_bool(inp_to_process)
        if solved:
            self.problem.solved = True
        self.menu.cf.add_problem_to_db(self.problem)
        self.menu.transition_to(MainMenuState())

    def _input_to_bool(self, inp):
        inp = inp.lower()
        t = ['yes', 'y', 'н', 'нуы', 'д', 'да']
        return inp in t


class ProjectEulerState(IMenuState):
    def show(self):
        super().show()
        print('NOT DONE YET (Press ENTER to continue...)')

    def process_input(self):
        input()
        self.menu.transition_to(MainMenuState())


class StatsState(IMenuState):
    def show(self):
        super().show()
        print('---------')
        print('All time stats:')
        print('---------')
        print(f'CodeForces: {len(self.menu.db.get_solved("cf"))} (solved),'
              f' {len(self.menu.db.get_not_solved("cf"))} (not solved)')
        print(f'ProjectEuler: {len(self.menu.db.get_solved("pe"))} (solved),'
              f' {len(self.menu.db.get_not_solved("pe"))} (not solved)')
        print('---------')

    def process_input(self):
        input('Press ENTER to go back...')
        self.menu.transition_to(MainMenuState())


class SettingsState(IMenuState):
    def show(self):
        super().show()
        print('\n'.join([
            f'1) Change name ({self.menu.db.user["name"]})',
            f'2) Change CodeForces level ({self.menu.db.user["cf_level"]})',
            f'3) Change CodeForces daily goal ({self.menu.db.user["cf_daily"]})',
            f'4) Change ProjectEuler level ({self.menu.db.user["pe_level"]})',
            f'5) Change ProjectEuler daily goal ({self.menu.db.user["pe_daily"]})',
            f'6) Back']))

    def process_input(self):
        s_choose = input()
        if len(s_choose) != 1 or not s_choose.isdigit():
            return
        s_choose = int(s_choose)
        if s_choose == 1:
            self.menu.db.update_user('name', input('New name: '))
        elif s_choose == 2:
            self.menu.db.update_user('cf_level', input('New CF level: '))
            self.menu.db.update_user('cf_page', 2)
        elif s_choose == 3:
            self.menu.db.update_user('cf_daily', input('New CF daily goal: '))
        elif s_choose == 4:
            self.menu.db.update_user('pe_level', input('New PE level: '))
        elif s_choose == 5:
            self.menu.db.update_user('pe_daily', input('New PE daily goal: '))
        elif s_choose == 6:
            self.menu.transition_to(MainMenuState())


class WelcomeState(IMenuState):
    def show(self):
        self._clear()
        print(welcome_message)

    def process_input(self):
        name = input('Enter your name: ')
        cf_level = input('Enter your CodeForces level (help for additional info): ')
        cf_daily = input('Enter number of CodeForces problems you will solve per day: ')
        pe_level = input('Enter your ProjectEuler level (help for additional info): ')
        pe_daily = input('Enter number of ProjectEuler problems you will solve per day: ')
        self.menu.db.new_user(name=name,
                              cf_level=cf_level,
                              pe_level=pe_level,
                              cf_daily=cf_daily,
                              pe_daily=pe_daily,
                              cf_page=2)


class MainMenuState(IMenuState):
    main_menu = {
        'CodeForces': CodeForcesState,
        'ProjectEuler': ProjectEulerState,
        'Stats': StatsState,
        'Settings': SettingsState,
        'Quit': None
    }

    def show(self):
        super().show()
        print(f'Welcome back, {self.menu.db.user["name"]}!')
        print('---------')
        print('Your today goals:')
        cf_solved, cf_goal = self.menu.cf.solved_today(), self.menu.cf.goal()
        if self.menu.cf.goal() != 0:
            print(f'CodeForces - {cf_solved}/{cf_goal}{multisolve(cf_solved, cf_goal)}')
        pe_solved, pe_goal = self.menu.pe.solved_today(), self.menu.pe.goal()
        if self.menu.pe.goal() != 0:
            print(f'ProjectEuler - {pe_solved}/{pe_goal}{multisolve(pe_solved, pe_goal)}')
        print('---------')
        self._show_menu()

    def process_input(self):
        inp = input()
        if len(inp) == 1 and inp.isdigit():
            choose = list(self.main_menu.keys())[int(inp) - 1]
            if choose == 'Quit':
                sys.exit()
            state = self.main_menu[choose]
            self.menu.transition_to(state())

    def _show_menu(self):
        print('\n'.join([f'{i + 1}) {x}' for i, x in enumerate(self.main_menu.keys())]))
