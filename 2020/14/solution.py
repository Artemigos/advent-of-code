import common

# part 1
setting_mask = 0
resetting_mask = ~0
mem = {}

for line in common.read_file('2020/14/data.txt').splitlines():
    if line[:4] == 'mask':
        mask_str = line[7:]
        setting_mask = int(mask_str.replace('X', '0'), 2)
        resetting_mask = int(mask_str.replace('X', '1'), 2)
    else: # mem[x] = y
        idx_str, val_str = line.replace('mem[', '').replace('] =', '').split()
        idx, val = int(idx_str), int(val_str)
        mem[idx] = (val | setting_mask) & resetting_mask

print(sum(mem.values()))

# part 2
import itertools

mask = ''
mem = {}

def gen_addresses(mask, addr, i=0):
    if i >= len(mask):
        yield []
        return
    rest = list(gen_addresses(mask, addr, i+1))
    shift = len(mask) - i - 1
    c = mask[shift]
    if c == '0':
        one_pointer = 1 << i
        digit = '1' if (addr & one_pointer) > 0 else '0'
        for rst in rest:
            yield rst + [digit]
    elif c == '1':
        for rst in rest:
            yield rst + ['1']
    else:
        for rst in rest:
            yield rst + ['0']
            yield rst + ['1']

for line in common.read_file('2020/14/data.txt').splitlines():
    if line[:4] == 'mask':
        mask = line[7:]
    else:
        idx_str, val_str = line.replace('mem[', '').replace('] =', '').split()
        idx, val = int(idx_str), int(val_str)
        for addr in gen_addresses(mask, idx):
            a = int(''.join(addr), 2)
            mem[a] = val

print(sum(mem.values()))
