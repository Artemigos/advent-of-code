import common

target = int(common.read_file().strip())

# part 1
mx = int(target/10)
arr = [0]*mx

for i in range(1, mx):
    if i > mx: break
    pts = i*10
    for step in range(i, mx, i):
        arr[step] += pts
        if arr[step] > target and step < mx:
            mx = step
            break

print(mx)

# part 2
mx = int(target/10)
arr = [0]*mx

for i in range(1, mx):
    if i > mx: break
    pts = i*11
    delivered = 0
    for step in range(i, mx, i):
        arr[step] += pts
        if arr[step] > target and step < mx:
            mx = step
            break
        delivered += 1
        if delivered >= 50:
            break

print(mx)
