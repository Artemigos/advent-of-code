from collections import deque

# part 1
def monkey(items, op, div_by, on_true, on_false):
    def _monkey(new_item=None):
        if new_item is not None:
            items.append(new_item)
        elif len(items) == 0:
            return None
        else:
            item = items.popleft()
            item = op(item)
            item //= 3
            if item % div_by == 0:
                return (item, on_true)
            else:
                return (item, on_false)
    return _monkey

monkeys = [
        monkey(deque([52, 60, 85, 69, 75, 75]), lambda x: x*17, 13, 6, 7),
        monkey(deque([96, 82, 61, 99, 82, 84, 85]), lambda x: x+8, 7, 0, 7),
        monkey(deque([95, 79]), lambda x: x+6, 19, 5, 3),
        monkey(deque([88, 50, 82, 65, 77]), lambda x: x*19, 2, 4, 1),
        monkey(deque([66, 90, 59, 90, 87, 63, 53, 88]), lambda x: x+7, 5, 1, 0),
        monkey(deque([92, 75, 62]), lambda x: x*x, 3, 3, 4),
        monkey(deque([94, 86, 76, 67]), lambda x: x+1, 11, 5, 2),
        monkey(deque([57]), lambda x: x+2, 17, 6, 2),
]

acc = [0]*len(monkeys)
for _ in range(20):
    for i in range(len(monkeys)):
        mk = monkeys[i]
        while True:
            item = mk()
            if item is None:
                break
            acc[i] = acc[i]+1
            monkeys[item[1]](item[0])

max_1 = max(acc)
acc.remove(max_1)
max_2 = max(acc)
print(max_1*max_2)

# part 2
def monkey(mod_by, items, op, div_by, on_true, on_false):
    def _monkey(new_item=None):
        if new_item is not None:
            items.append(new_item)
        elif len(items) == 0:
            return None
        else:
            item = items.popleft()
            item = op(item)
            item %= mod_by
            if item % div_by == 0:
                return (item, on_true)
            else:
                return (item, on_false)
    return _monkey

mod_by = 13*7*19*2*5*3*11*17
monkeys = [
        monkey(mod_by, deque([52, 60, 85, 69, 75, 75]), lambda x: x*17, 13, 6, 7),
        monkey(mod_by, deque([96, 82, 61, 99, 82, 84, 85]), lambda x: x+8, 7, 0, 7),
        monkey(mod_by, deque([95, 79]), lambda x: x+6, 19, 5, 3),
        monkey(mod_by, deque([88, 50, 82, 65, 77]), lambda x: x*19, 2, 4, 1),
        monkey(mod_by, deque([66, 90, 59, 90, 87, 63, 53, 88]), lambda x: x+7, 5, 1, 0),
        monkey(mod_by, deque([92, 75, 62]), lambda x: x*x, 3, 3, 4),
        monkey(mod_by, deque([94, 86, 76, 67]), lambda x: x+1, 11, 5, 2),
        monkey(mod_by, deque([57]), lambda x: x+2, 17, 6, 2),
]

acc = [0]*len(monkeys)
for _ in range(10000):
    for i in range(len(monkeys)):
        mk = monkeys[i]
        while True:
            item = mk()
            if item is None:
                break
            acc[i] = acc[i]+1
            monkeys[item[1]](item[0])

max_1 = max(acc)
acc.remove(max_1)
max_2 = max(acc)
print(max_1*max_2)
