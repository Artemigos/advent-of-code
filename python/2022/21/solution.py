import common

lines = common.read_file().splitlines()

monkeys = dict()

# part 1
def gen_op(monkeys, m1, m2, op):
    def f():
        if op == '+':
            return monkeys[m1]() + monkeys[m2]()
        elif op == '-':
            return monkeys[m1]() - monkeys[m2]()
        elif op == '*':
            return monkeys[m1]() * monkeys[m2]()
        elif op == '/':
            return monkeys[m1]() // monkeys[m2]()
        else:
            raise '???'
    return f

def gen_const(v):
    def f():
        return v
    return f

for line in lines:
    seg = line.split(': ')
    k = seg[0]
    if seg[1].isdigit():
        v = int(seg[1])
        monkeys[k] = gen_const(v)
    else:
        seg = seg[1].split(' ')
        op = seg[1]
        monkeys[k] = gen_op(monkeys, seg[0], seg[2], op)

print(monkeys['root']())

# part 2

# TODO:
# - build operation tree
# - convert equation to get just 'x' on one side
# - eval

monkeys_m = dict()
for line in lines:
    seg = line.split(': ')
    k = seg[0]
    if seg[1].isdigit():
        v = int(seg[1])
        monkeys_m[k] = (True, v)
    else:
        seg = seg[1].split(' ')
        op = seg[1]
        monkeys_m[k] = (False, seg[0], seg[2], op)

me = 'humn'
root_l = monkeys_m['root'][1]
root_r = monkeys_m['root'][2]

#rev = dict()
#curr = me
#while curr != root_l and curr != root_r:
#    for k in monkeys_m:
#        mon = monkeys_m[k]
#        if mon[0]:
#            #if k != me:
#            #    rev[k] = (True, mon[1])
#            continue
#
#        _, m1, m2, op = monkeys_m[k]
#        if m1 == curr or m2 == curr:
#            other = m1 if m2 == curr else m2
#            if op == '+':
#                rev_op = '-'
#            elif op == '-':
#                rev_op = '+'
#            elif op == '*':
#                rev_op = '/'
#            elif op == '/':
#                rev_op = '*'
#            else:
#                raise '???'
#            if curr == m1 or op in ['+','*']:
#                rev[curr] = (False, k, other, rev_op)
#            else:
#                rev[curr] = (False, other, k, rev_op)
#            curr = k
#            break
#
#if curr == root_l:
#    rev[root_l] = (True, monkeys[root_r]())
#    print('ROOT L', rev[root_l])
#else:
#    rev[root_r] = (True, monkeys[root_l]())
#    print('ROOT R', rev[root_r])
#
#for k in monkeys_m:
#    if k not in rev:
#        rev[k] = monkeys_m[k]
#
#rev_f = dict()
#for k in rev:
#    mon = rev[k]
#    if mon[0]:
#        rev_f[k] = gen_const(mon[1])
#        continue
#
#    _, m1, m2, op = mon
#    rev_f[k] = gen_op(rev_f, m1, m2, op)
#
#print(rev_f[me]())
#
#evaled = dict()
#
#while True:
#    for k in rev:
#        mon = rev[k]
#        if k in evaled:
#            continue
#        if mon[0]:
#            print('add const', k, mon[1])
#            evaled[k] = mon[1]
#            continue
#        _, m1, m2, op = mon
#        if m1 not in evaled or m2 not in evaled:
#            continue
#        if op == '+':
#            val = evaled[m1] + evaled[m2]
#        elif op == '-':
#            val = evaled[m1] - evaled[m2]
#        elif op == '*':
#            val = evaled[m1] * evaled[m2]
#        elif op == '/':
#            val = evaled[m1] / evaled[m2]
#        else:
#            raise '???'
#        print('add op', k, '=', m1, op, m2, '=', evaled[m1], op, evaled[m2], '=', val)
#        evaled[k] = val
#        if k == me:
#            break
#    else:
#        continue
#    break
#
#print(evaled[me])

evaled = dict()

def gen_print_op(monkeys, m1, m2, op):
    def f():
        v1 = monkeys[m1]()
        v2 = monkeys[m2]()
        if isinstance(v1, str) or isinstance(v2, str):
            return '('+str(v1)+op+str(v2)+')'
        elif op == '+':
            return v1 + v2
        elif op == '-':
            return v1 - v2
        elif op == '*':
            return v1 * v2
        elif op == '/':
            return v1 // v2
        else:
            raise '???'
    return f

print_f = dict()
for k in monkeys_m:
    mon = monkeys_m[k]
    if mon[0]:
        if k == me:
            print_f[k] = lambda: 'x'
        else:
            print_f[k] = gen_const(mon[1])
        continue

    _, m1, m2, op = mon
    print_f[k] = gen_print_op(print_f, m1, m2, op)

print(print_f[root_l]())
print(print_f[root_r]())
