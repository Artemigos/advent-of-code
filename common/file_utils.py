import re

def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def split_table(data: str, separator='\t'):
    lines = data.splitlines()
    return list(map(lambda x: x.split(separator), lines))


def flat_map(func, data):
    for el in data:
        for inner in func(el):
            yield inner


def split_flat(data: str):
    lines = data.splitlines()
    return list(flat_map(lambda x: x.split(' '), lines))


def to_int(data: list):
    return list(map(int, data))


def to_ord(data: str):
    return list(map(ord, data))


def extract_numbers(data: str):
    return [int(x) for x in re.findall(r'-?\d+', data)]


def extract_words(data: str):
    return re.findall(r'\w+', data)


def import_from_day(year, day, module):
    year = str(year)
    day = str(day)
    y = __import__(f'{year}.{day}.{module}')
    d = getattr(y, day)
    return getattr(d, module)


def import_from_year(year, module):
    year = str(year)
    y = __import__(f'{year}.{module}')
    return getattr(y, module)


def import_solution(year, day):
    return import_from_day(year, day, 'solution')


def import_year_common(year):
    return import_from_year(year, 'year_common')


def print_and_return(*args):
    print(*args, end='\r')
