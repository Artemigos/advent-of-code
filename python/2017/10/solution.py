import common
year_common = common.import_year_common(2017)

data = common.read_file('2017/10/data.txt').strip()
ints = common.to_int(data.split(','))

# NOTE: implementation of knot hash was moved to common

# part 1
result = year_common.knot_hash(ints)
print(result[0] * result[1])

# part 2
_, representation = year_common.knot_hash_full(data)
print(representation)
