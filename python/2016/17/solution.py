import hashlib
import queue
import common

data = bytes(common.read_file().strip(), encoding='utf8')
# data = b'ihgpwlah' # sample
board_size = 4, 4
target = 3, 3
characters_for_open = ['b', 'c', 'd', 'e', 'f']

md5 = hashlib.md5(data)
q = queue.deque([(b'', (0, 0), md5)])

found_shortest = False
last_path = None
while len(q) > 0:
    path, position, hash_gen = q.popleft()
    if position == target:
        if not found_shortest:
            print(str(path, encoding='utf8'))
            found_shortest = True
        last_path = path # part 2
        continue

    my_hash_gen = md5.copy()
    if len(path) > 0:
        my_hash_gen.update(path)
    my_hash = my_hash_gen.hexdigest()

    if my_hash[0] in characters_for_open and position[1] > 0:
        q.append((path+b'U', (position[0], position[1]-1), my_hash_gen))
    if my_hash[1] in characters_for_open and position[1] < board_size[1]-1:
        q.append((path+b'D', (position[0], position[1]+1), my_hash_gen))
    if my_hash[2] in characters_for_open and position[0] > 0:
        q.append((path+b'L', (position[0]-1, position[1]), my_hash_gen))
    if my_hash[3] in characters_for_open and position[0] < board_size[0]-1:
        q.append((path+b'R', (position[0]+1, position[1]), my_hash_gen))

print(len(last_path))
