import cProfile


def profile_entry():
    solution = __import__('2017.16.solution')
    return solution


cProfile.run('profile_entry()')
