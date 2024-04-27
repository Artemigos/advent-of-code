import common
import queue
from collections import Counter

# 478 players; last marble is worth 71240 points
nplayers = 478
last_marble = 71240

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
