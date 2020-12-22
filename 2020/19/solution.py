import lark
import re
import common

lines = common.read_file('2020/19/data.txt').splitlines()
divider = lines.index('')
rules_str = lines[:divider]
tickets = lines[divider+1:]
grammar = ''

for line in rules_str:
    new_line = re.sub(r'(\d+)', r'rule\1', line)
    grammar += new_line + '\n'

# part 1
lrk = lark.Lark(grammar, start='rule0')
acc = 0
for t in tickets:
    try:
        lrk.parse(t)
        acc += 1
    except:
        pass

print(acc)

# part 2
grammar = re.sub(r'rule8:.*\n', 'rule8: rule42 | rule42 rule8\n', grammar)
grammar = re.sub(r'rule11:.*\n', 'rule11: rule42 rule31 | rule42 rule11 rule31\n', grammar)
lrk = lark.Lark(grammar, start='rule0')

acc = 0
for t in tickets:
    try:
        lrk.parse(t)
        acc += 1
    except:
        pass

print(acc)
