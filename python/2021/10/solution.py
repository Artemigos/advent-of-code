import common

lines = common.read_file().splitlines()

# part 1 and 2

match = {
    ')': '(',
    '}': '{',
    ']': '[',
    '>': '<'
}
score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
score_completion = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

acc = 0
completion_scores = []
for line in lines:
    stack = []
    for c in line:
        if c in ['(', '{', '[', '<']:
            stack.append(c)
        else: # closing
            if stack[-1] == match[c]:
                stack.pop()
            else: # corrupted
                acc += score[c]
                break
    else: # incomplete
        c_acc = 0
        while len(stack) > 0:
            c = stack.pop()
            c_acc *= 5
            c_acc += score_completion[c]
        completion_scores.append(c_acc)

print(acc)

completion_scores = sorted(completion_scores)
print(completion_scores[len(completion_scores)//2])
