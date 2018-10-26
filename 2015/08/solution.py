import common
import re

lines = common.read_file('2015/08/data.txt').splitlines()

# part 1
diff = 0
for line in lines:
    org_len = len(line)
    line = line[1:-1]
    line = line.replace('\\\\', '_')
    line = line.replace('\\"', '"')
    line = re.sub('\\\\x[0-9a-fA-F]{2}', '_', line)
    diff += org_len - len(line)

print(diff)

# part 2
diff = 0
for line in lines:
    result = '"'
    for c in line:
        if c == '"' or c == '\\':
            result += '\\'
        result += c
    result += '"'
    diff += len(result) - len(line)

print(diff)
