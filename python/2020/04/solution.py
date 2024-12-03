import re
import common

lines = common.read_file().splitlines()

passports = []
current_passport = {}

for l in lines:
    if l == '':
        passports.append(current_passport)
        current_passport = {}
        continue

    fields = l.split(' ')
    for f in fields:
        (key, val) = f.split(':')
        current_passport[key] = val

passports.append(current_passport)
current_passport = {}

# part 1
required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

passports_with_required_fields = []
for p in passports:
    all_found = True
    for f in required_fields:
        if f not in p:
            all_found = False
            break
    if all_found:
        passports_with_required_fields.append(p)

print(len(passports_with_required_fields))

# part 2
def validate(p):
    byr, iyr, eyr, hgt, hcl, ecl, pid = \
        p['byr'], p['iyr'], p['eyr'], p['hgt'], \
        p['hcl'], p['ecl'], p['pid']

    if not re.fullmatch(r'\d{4}', byr): return False
    byr = int(byr)
    if byr < 1920 or byr > 2002: return False
    if not re.fullmatch(r'\d{4}', iyr): return False
    iyr = int(iyr)
    if iyr < 2010 or iyr > 2020: return False
    if not re.fullmatch(r'\d{4}', eyr): return False
    eyr = int(eyr)
    if eyr < 2020 or eyr > 2030: return False
    if not re.fullmatch(r'\d+(cm|in)', hgt): return False
    hgt_unit = hgt[-2:]
    hgt = int(hgt[:-2])
    if hgt_unit == 'cm' and (hgt < 150 or hgt > 193): return False
    elif hgt_unit == 'in' and (hgt < 59 or hgt > 76): return False
    if not re.fullmatch(r'#[0-9a-f]{6}', hcl): return False
    if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']: return False
    if not re.fullmatch(r'\d{9}', pid): return False

    return True

amount = 0
for p in passports_with_required_fields:
    if validate(p):
        amount += 1

print(amount)
