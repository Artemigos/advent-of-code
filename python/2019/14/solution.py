import common
from collections import defaultdict
import math

data = common.read_file().splitlines()
rules = {}
ore = 'ORE'
fuel = 'FUEL'

for line in data:
    left, right = line.split(' => ')
    ingredients = left.split(', ')
    ingr = []
    for i in ingredients:
        num, name = i.split(' ')
        ingr.append((int(num), name))
    num, name = right.split(' ')
    rules[name] = ingr, (int(num), name)

# part 1
def find_needed(fuel_amount):
    needed = defaultdict(lambda: 0, {fuel: fuel_amount})
    produced = defaultdict(lambda: 0)

    def check_if_all_produced():
        for k in needed:
            if k != ore and produced[k] < needed[k]:
                return False
        return True

    while not check_if_all_produced():
        for k in list(needed.keys()):
            if k != ore and produced[k] < needed[k]:
                ingredients, result = rules[k]
                amount_produced, _ = result
                mul = math.ceil((needed[k]-produced[k])/amount_produced)
                for amount, name in iter(ingredients):
                    needed[name] += amount*mul
                produced[k] += amount_produced*mul

    return needed

needed = find_needed(1)
print(needed[ore])

# part 2
ore_amount = 1000000000000
productions = ore_amount//needed[ore]
prod_min = productions
prod_max = productions+1

while find_needed(prod_max)[ore] < ore_amount:
    prod_max <<= 1

while True:
    middle = (prod_max-prod_min)//2+prod_min
    middle_needed = find_needed(middle)[ore]
    if middle_needed < ore_amount:
        prod_min = middle
    elif middle_needed > ore_amount:
        prod_max = middle
    else:
        print(middle)
        break

    if prod_min == prod_max or prod_max - prod_min == 1:
        max_needed = find_needed(prod_max)[ore]
        if max_needed <= ore_amount:
            result = prod_max
        else:
            result = prod_min
        print(result)
        break
