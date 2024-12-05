import common

rules_data, updates = common.read_file().split('\n\n')
rules_data = rules_data.splitlines()
updates = updates.splitlines()

rules = set()
for rule in rules_data:
    l, r = rule.split('|')
    rules.add((l, r))

def is_correct(nums):
    for i in range(len(nums)-1):
        for j in range(i+1, len(nums)):
            if (nums[j], nums[i]) in rules:
                return False
    return True

# part 1
incorrect_nums = []
acc = 0
for update in updates:
    nums = update.split(',')
    if is_correct(nums):
        acc += int(nums[len(nums)//2])
    else:
        incorrect_nums.append(nums)

print(acc)

# part 2
acc = 0
for nums in incorrect_nums:
    applicable_rules = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            rule = (nums[i], nums[j])
            if rule in rules:
                applicable_rules.append(rule)
            rule = (nums[j], nums[i])
            if rule in rules:
                applicable_rules.append(rule)

    deps = {}
    for rule in applicable_rules:
        l, r = rule
        if r not in deps:
            deps[r] = set()
        deps[r].add(l)

    ordered = []
    def add(num):
        if num in ordered:
            return
        if num in deps:
            for dep in deps[num]:
                add(dep)
        ordered.append(num)
    for num in nums:
        add(num)

    acc += int(ordered[len(ordered)//2])

print(acc)

