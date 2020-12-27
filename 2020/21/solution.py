from collections import defaultdict
import common

lines = common.read_file('2020/21/data.txt').splitlines()

can_be_contained_by_ingredients = {}
all_ingredients = defaultdict(int)
all_allergens = set()

for line in lines:
    ingredients, allergens = line.rstrip(')').split(' (contains ')
    ingredients = ingredients.split(' ')
    allergens = allergens.split(', ')

    for a in allergens:
        all_allergens.add(a)
        if a in can_be_contained_by_ingredients:
            can_be_contained_by_ingredients[a] = can_be_contained_by_ingredients[a].intersection(ingredients)
        else:
            can_be_contained_by_ingredients[a] = set(ingredients)

    for i in ingredients:
        all_ingredients[i] += 1

# part 1
ingredients_acc = set(all_ingredients)
for k in can_be_contained_by_ingredients:
    ingr = can_be_contained_by_ingredients[k]
    cannot_contain = set(all_ingredients.keys()).difference(ingr)
    ingredients_acc = ingredients_acc.intersection(cannot_contain)

print(sum(v for k, v in all_ingredients.items() if k in ingredients_acc))

# part 2
known = {}

while sum(len(v) for k, v in can_be_contained_by_ingredients.items()) > len(all_allergens):
    for k in known:
        v = known[k]
        for k2 in can_be_contained_by_ingredients:
            v2 = can_be_contained_by_ingredients[k2]
            if k != k2 and v in v2:
                v2.remove(v)

    for k in can_be_contained_by_ingredients:
        if k in known:
            continue
        v = can_be_contained_by_ingredients[k]
        if len(v) == 1:
            known[k] = list(v)[0]

keys = sorted(known.keys())
ordered_ingredients = [known[k] for k in keys]
print(','.join(ordered_ingredients))
