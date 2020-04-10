import os

from octo_train.db import Database
from octo_train.codeforces import CodeForces
from octo_train.euler import ProjectEuler
from octo_train.colored import welcome_message, logo, multisolve


menu = [
    'CodeForces',
    'ProjectEuler',
    'Stats',
    'Settings',
    'Quit'
]


def show_menu():
    for i, item in enumerate(menu):
        print(i + 1, ') ', item, sep='')
    while True:
        inp = input()
        if len(inp) == 1 and inp.isdigit():
            return menu[int(inp) - 1]


def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def input_to_bool(inp):
    inp = inp.lower()
    t = ['yes', 'y', 'н', 'нуы', 'д', 'да']
    return inp in t


def main():
    clear()
    db = Database()
    if not db.loaded:
        print(welcome_message)
        name = input('Enter your name: ')
        cf_level = input('Enter your CodeForces level (help for additional info): ')
        cf_daily = input('Enter number of CodeForces problems you will solve per day: ')
        pe_level = input('Enter your ProjectEuler level (help for additional info): ')
        pe_daily = input('Enter number of ProjectEuler problems you will solve per day: ')
        db.new_user(name=name, cf_level=cf_level, pe_level=pe_level, cf_daily=cf_daily, pe_daily=pe_daily, cf_page=2)
    cf = CodeForces(db)
    pe = ProjectEuler(db)
    while True:
        clear()
        print(logo)
        print(f'Welcome back, {db.user["name"]}!')
        print('---------')
        print('Your today goals:')
        cf_solved, cf_goal = cf.solved_today(), cf.goal()
        if cf.goal() != 0:
            print(f'CodeForces - {cf_solved}/{cf_goal}{multisolve(cf_solved, cf_goal)}')
        pe_solved, pe_goal = pe.solved_today(), pe.goal()
        if pe.goal() != 0:
            print(f'ProjectEuler - {pe_solved}/{pe_goal}{multisolve(pe_solved, pe_goal)}')
        print('---------')

        choose = show_menu()
        if choose == 'CodeForces':
            clear()
            print(logo)
            problem = cf.get_problem()
            print(problem.title, f'({problem.difficulty})')
            print(problem.link)
            solved = input_to_bool(input('Solved? (y/n): '))
            if solved:
                problem.solved = True
            cf.add_problem_to_db(problem)
        elif choose == 'ProjectEuler':
            clear()
            print(logo)
            print('NOT DONE YET (Press ENTER to continue...)')
            input()
        elif choose == 'Stats':
            clear()
            print(logo)
            print('---------')
            print('All time stats:')
            print('---------')
            print(f'CodeForces: {len(db.get_solved("cf"))} (solved), {len(db.get_not_solved("cf"))} (not solved)')
            print(f'ProjectEuler: {len(db.get_solved("pe"))} (solved), {len(db.get_not_solved("pe"))} (not solved)')
            print('---------')
            input('Press ENTER to go back...')
        elif choose == 'Settings':
            while True:
                clear()
                print(logo)
                print('\n'.join([
                    f'1) Change name ({db.user["name"]})',
                    f'2) Change CodeForces level ({db.user["cf_level"]})',
                    f'3) Change CodeForces daily goal ({db.user["cf_daily"]})',
                    f'4) Change ProjectEuler level ({db.user["pe_level"]})',
                    f'5) Change ProjectEuler daily goal ({db.user["pe_daily"]})',
                    f'6) Back']))
                s_choose = input()
                if len(s_choose) != 1 or not s_choose.isdigit():
                    continue
                s_choose = int(s_choose)
                if s_choose == 1:
                    db.update_user('name', input('New name: '))
                elif s_choose == 2:
                    db.update_user('cf_level', input('New CF level: '))
                elif s_choose == 3:
                    db.update_user('cf_daily', input('New CF daily goal: '))
                elif s_choose == 4:
                    db.update_user('pe_level', input('New PE level: '))
                elif s_choose == 5:
                    db.update_user('pe_daily', input('New PE daily goal: '))
                elif s_choose == 6:
                    break
        elif choose == 'Quit':
            clear()
            break


if __name__ == '__main__':
    main()
