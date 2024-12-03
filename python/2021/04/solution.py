import common

lines = common.read_file().splitlines()
randoms = common.to_int(lines[0].split(','))

boards = []
curr_line = 2
while curr_line+4 < len(lines):
    board = set(), [set(), set(), set(), set(), set()]
    for _ in range(5):
        nums = common.to_int(lines[curr_line].split())
        row = set(nums)
        for col in range(5):
            n = nums[col]
            board[0].add(n)
            board[1][col].add(n)
        board[1].append(row)
        curr_line += 1
    boards.append(board)
    curr_line += 1

# part 1 and 2

scores = []
for i in range(len(randoms)):
    selected = set(randoms[:i+1])
    won = []
    for board in boards:
        for winning_set in board[1]:
            if selected.issuperset(winning_set):
                last_num = randoms[i]
                not_selected = board[0].difference(selected)
                result = sum(not_selected) * last_num
                scores.append(result)
                won.append(board)
                break
    for board in won:
        boards.remove(board)

print(scores[0])
print(scores[-1])
