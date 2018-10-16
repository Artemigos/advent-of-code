def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def split_table(data: str, separator='\t'):
    lines = data.splitlines()
    return list(map(lambda x: x.split(separator), lines))

def flatmap(func, data):
    for el in data:
        for inner in func(el):
            yield inner

def split_flat(data: str):
    lines = data.splitlines()
    return list(flatmap(lambda x: x.split(' '), lines))

def to_int(data: list):
    return list(map(int, data))

def to_ord(data: str):
    return list(map(ord, data))

def import_from_day(year, day, module):
    year = str(year)
    day = str(day)
    y = __import__(f'{year}.{day}.{module}')
    d = getattr(y, day)
    return getattr(d, module)

def import_solution(year, day):
    return import_from_day(year, day, 'solution')

def print_and_return(*args):
    print(*args, end='\r')
