# capacity, durability, flavor, texture, calories
ingredients = dict (
    Sugar=(3, 0, 0, -3, 2),
    Sprinkles=(-3, 3, 0, 0, 9),
    Candy=(-1, 0, 4, 0, 1),
    Chocolate=(0, 0, -2, 2, 8),
)

amount = 100

def sum_characteristic(i, sugar, sprinkles, candy, choco):
    characteristic = 0
    characteristic += sugar * ingredients['Sugar'][i]
    characteristic += sprinkles * ingredients['Sprinkles'][i]
    characteristic += candy * ingredients['Candy'][i]
    characteristic += choco * ingredients['Chocolate'][i]
    return max([characteristic, 0])

def calc_score(sugar, sprinkles, candy, choco):
    capacity = sum_characteristic(0, sugar, sprinkles, candy, choco)
    durability = sum_characteristic(1, sugar, sprinkles, candy, choco)
    flavor = sum_characteristic(2, sugar, sprinkles, candy, choco)
    texture = sum_characteristic(3, sugar, sprinkles, candy, choco)
    return capacity * durability * flavor * texture

# part 1
max_score = 0
for sugar in range(amount+1):
    for sprinkles in range(amount+1):
        if sugar + sprinkles > amount:
            break
        for candy in range(amount+1):
            if sugar + sprinkles + candy > amount:
                break
            for choco in range(amount+1):
                if sugar + sprinkles + candy + choco > amount:
                    break
                score = calc_score(sugar, sprinkles, candy, choco)
                if score > max_score:
                    max_score = score

print(max_score)

# part 2
max_score = 0
for sugar in range(amount+1):
    for sprinkles in range(amount+1):
        if sugar + sprinkles > amount:
            break
        for candy in range(amount+1):
            if sugar + sprinkles + candy > amount:
                break
            for choco in range(amount+1):
                if sugar + sprinkles + candy + choco > amount:
                    break
                calorie = sum_characteristic(4, sugar, sprinkles, candy, choco)
                if calorie != 500:
                    continue
                score = calc_score(sugar, sprinkles, candy, choco)
                if score > max_score:
                    max_score = score

print(max_score)
