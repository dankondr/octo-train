import colorful as cf

logo = '''{c.bold}{c.pink}\
              __              __             _     
  ____  _____/ /_____        / /__________ _(_)___ 
 / __ \/ ___/ __/ __ \______/ __/ ___/ __ `/ / __ \\
/ /_/ / /__/ /_/ /_/ /_____/ /_/ /  / /_/ / / / / /
\____/\___/\__/\____/      \__/_/   \__,_/_/_/ /_/ {c.reset}'''.format(c=cf)

welcome_message = f'''\
                    Welcome to
{logo}
An individual programming trainer for everyone.'''


def multisolve(solved, goal):
    diff = solved - goal
    if diff < 0:
        return ''
    phrases = [
        '',
        'Dominating',
        'Rampage',
        'Mega Solve',
        'Unstoppable',
        'Wicked Sick',
        'Monster Solve',
        'Godlike',
        'Beyond Godlike',
    ]
    phrase = ' {c.yellow}(Goal completed){c.bold}{c.red} '.format(c=cf)
    phrase += phrases[min(diff, len(phrases) - 1)].upper() + str(cf.reset)
    return phrase
