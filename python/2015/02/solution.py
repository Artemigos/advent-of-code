import common

lines = common.read_file('2015/02/data.txt').splitlines()

area_acc = 0
ribbon_acc = 0

for line in lines:
    segments = line.split('x')
    sides = list(map(int, segments))

    area1 = sides[0] * sides[1]
    area2 = sides[0] * sides[2]
    area3 = sides[1] * sides[2]

    min_area = min([area1, area2, area3])
    area_acc += (2*area1 + 2*area2 + 2*area3 + min_area)

    perimeter1 = 2*sides[0] + 2*sides[1]
    perimeter2 = 2*sides[0] + 2*sides[2]
    perimeter3 = 2*sides[1] + 2*sides[2]

    min_perimeter = min([perimeter1, perimeter2, perimeter3])
    volume = sides[0] * sides[1] * sides[2]

    ribbon_acc += (min_perimeter + volume)

print(area_acc)
print(ribbon_acc)
