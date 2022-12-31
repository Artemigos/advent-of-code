import common
from collections import deque
from ast import literal_eval
from math import lcm

lines = common.read_file().splitlines()

class Monkey:
    def __init__(self, items: list, op, div_by, on_true, on_false, limiter):
        self.items = deque(items)
        self.op = op
        self.div_by = div_by
        self.on_true = on_true
        self.on_false = on_false
        self.limiter = limiter

    def add(self, new_item):
        self.items.append(new_item)

    def process(self):
        if len(self.items) == 0:
            return None
        else:
            item = self.items.popleft()
            item = self.op(item)
            item = self.limiter(item)
            if item % self.div_by == 0:
                return (item, self.on_true)
            else:
                return (item, self.on_false)

def parse(lines, limiter):
    monkeys = []
    for i in range(0, len(lines), 7):
        items = lines[i+1].split(': ')[1]
        items = literal_eval('[' + items + ']')
        op = lines[i+2].split(' = ')[1]
        op = eval('lambda old: ' + op)
        div_by = int(lines[i+3].split(' ')[-1])
        on_true = int(lines[i+4].split(' ')[-1])
        on_false = int(lines[i+5].split(' ')[-1])
        monkeys.append(Monkey(items, op, div_by, on_true, on_false, limiter))
    return monkeys

# part 1
monkeys = parse(lines, lambda x: x // 3)
acc = [0]*len(monkeys)
for _ in range(20):
    for i in range(len(monkeys)):
        mk = monkeys[i]
        while True:
            item = mk.process()
            if item is None:
                break
            acc[i] = acc[i]+1
            monkeys[item[1]].add(item[0])

max_1 = max(acc)
acc.remove(max_1)
max_2 = max(acc)
print(max_1*max_2)

# part 2
mod_by = lcm(*map(lambda x: x.div_by, monkeys))
monkeys = parse(lines, lambda x: x % mod_by)
acc = [0]*len(monkeys)
for _ in range(10000):
    for i in range(len(monkeys)):
        mk = monkeys[i]
        while True:
            item = mk.process()
            if item is None:
                break
            acc[i] = acc[i]+1
            monkeys[item[1]].add(item[0])

max_1 = max(acc)
acc.remove(max_1)
max_2 = max(acc)
print(max_1*max_2)
