import common
import queue
from collections import Counter

# 478 players; last marble is worth 71240 points
nums = common.extract_numbers(common.read_file())
nplayers = nums[0]
last_marble = nums[1]

circle = queue.deque([0])
scores = Counter()

for i in range(1, last_marble+1):
    curr_player = (i-1)%nplayers
    if i%23 != 0:
        circle.rotate(-2)
        circle.appendleft(i)
    else:
        circle.rotate(7)
        scores[curr_player] += i
        removed = circle.popleft()
        scores[curr_player] += removed

print(max(scores.values()))

circle = queue.deque([0])
scores = Counter()

for i in range(1, (last_marble*100)+1):
    curr_player = (i-1)%nplayers
    if i%23 != 0:
        circle.rotate(-2)
        circle.appendleft(i)
    else:
        circle.rotate(7)
        scores[curr_player] += i
        removed = circle.popleft()
        scores[curr_player] += removed

print(max(scores.values()))
