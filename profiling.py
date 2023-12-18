import cProfile
import sys


if len(sys.argv) != 2:
    print('Usage:')
    print('\tpython3 -m profiling <module>')
    print()
    print('Example:')
    print('\tpython3 -m profiling 2017.16.solution')
    exit(1)


def profile_entry():
    solution = __import__(module)
    return solution


cProfile.run('profile_entry()')
