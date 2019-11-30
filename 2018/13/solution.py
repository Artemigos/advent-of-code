import collections as coll
import queue
import itertools
import functools
import numpy as np
import re

def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def read_lines(path: str) -> str:
    with open(path) as f:
        return f.read().splitlines()

def extract_words(data: str):
    return re.findall(r'\w+', data)

def extract_numbers(data: str):
    return [int(x) for x in re.findall(r'-?\d+', data)]

def parse_line(line: str):
    return line

data = read_file('2018/13/data.txt').splitlines()
parsed = [parse_line(x) for x in data]

def is_cart(c):
    return c == '<' or c == '>' or c == '^' or c == 'v'

carts = []
for y in range(len(parsed)):
    row = parsed[y]
    for x in range(len(row)):
        c = row[x]
        if is_cart(c):
            carts.append([ x, y, c, 'l', True ])

for y in range(len(parsed)):
    parsed[y] = parsed[y].replace('^', '|')
    parsed[y] = parsed[y].replace('<', '-')
    parsed[y] = parsed[y].replace('>', '-')
    parsed[y] = parsed[y].replace('v', '|')

def next_pos(cart):
    x, y, c, *rest = cart

    if c == '<':
        return x-1, y
    if c == '>':
        return x+1, y
    if c == '^':
        return x, y-1
    return x, y+1

rotation_slash = {
    '^': '<', '>': 'v', 'v': '>', '<': '^'
}

rotation_backslash = {
    '^': '>', '<': 'v', 'v': '<', '>': '^'
}

rotation_r = {
    '^': '>', '>': 'v', 'v': '<', '<': '^'
}

rotation_l = {
    '^': '<', '<': 'v', 'v': '>', '>': '^'
}

def next_dir(cart, nxt_pos):
    # print(cart, nxt_pos)
    field = parsed[nxt_pos[1]][nxt_pos[0]]
    assert field != ' ', 'stepped on wrong field'
    if field == '-' or field == '|':
        return cart[2], cart[3]
    if field == '\\':
        return rotation_slash[cart[2]], cart[3]
    if field == '/':
        return rotation_backslash[cart[2]], cart[3]
    if field == '+':
        nxt_turn = cart[3]
        if nxt_turn == 'l':
            return rotation_l[cart[2]], 's'
        if nxt_turn == 's':
            return cart[2], 'r'
        if nxt_turn == 'r':
            return rotation_r[cart[2]], 'l'
    assert False, 'unexpected case reached'

def collision(nxt_pos):
    for crt in carts:
        if crt[4] and crt[0] == nxt_pos[0] and crt[1] == nxt_pos[1]:
            crt[4] = False
            return True
    return False

while True:
    for cart in carts:
        if not cart[4]:
            continue
        nxt_pos = next_pos(cart)
        if collision(nxt_pos):
            # print('crash at', nxt_pos)
            # exit(0)
            cart[4] = False
            continue
        nxt_dir = next_dir(cart, nxt_pos)
        cart[0] = nxt_pos[0]
        cart[1] = nxt_pos[1]
        cart[2] = nxt_dir[0]
        cart[3] = nxt_dir[1]

    alive = list(filter(lambda x: x[4], carts))
    if len(alive) == 1:
        print('last cart', alive[0])
        break
    carts = list(sorted(alive, key=lambda x:str(x[1]).rjust(3, '0')+str(x[0]).rjust(3, '0')))
