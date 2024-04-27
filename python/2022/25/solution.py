import common
from functools import reduce

to_dec_digit = { '=': -2, '-': -1, '0': 0, '1': 1, '2': 2 }
to_snafu_digit = { -2: '=', -1: '-', 0: '0', 1: '1', 2: '2' }
def to_dec(num):
    return reduce(lambda acc, c: acc * 5 + to_dec_digit[c], num, 0)
def to_snafu(num):
    result = ''
    while num > 0:
        rem = num % 5
        if rem > 2:
            rem -= 5
        result = to_snafu_digit[rem] + result
        num = (num - rem) // 5
    return result

result = sum((to_dec(line) for line in common.read_file().splitlines()))
print(to_snafu(result))
