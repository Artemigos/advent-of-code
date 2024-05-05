class Group:
    def __init__(self, units, hp, weaknesses, immunities, damage, damage_type, initiative):
        self.units = units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.damage = damage
        self.damage_type = damage_type
        self.initiative = initiative

    def get_effective_power(self):
        return self.units * self.damage

    def is_dead(self):
        return self.units <= 0

    def calculate_received_damage(self, group):
        if group.damage_type in self.immunities:
            return 0
        damage = group.get_effective_power()
        if group.damage_type in self.weaknesses:
            damage *= 2

        return damage

    def take_damage(self, group):
        damage = self.calculate_received_damage(group)
        units_dead = damage // self.hp
        units_dead = min(units_dead, self.units)
        self.units -= units_dead
        return units_dead

class Force:
    def __init__(self, groups):
        self.groups = groups

    def is_dead(self):
        for group in self.groups:
            if not group.is_dead():
                return False
        return True

# let's have some fun parsing this
def parse_forces(data: str) -> tuple[Force, Force]:
    import parsy as p
    word = p.regex(r'\b\w+?\b')
    number = p.regex(r'\d+').map(int)
    @p.generate
    def file():
        yield p.string('Immune System:\n')
        immune_groups = yield line.sep_by(p.string('\n'))
        yield p.string('\n\nInfection:\n')
        infection_groups = yield line.sep_by(p.string('\n'))
        yield p.string('\n').optional()
        return Force(immune_groups), Force(infection_groups)
    @p.generate
    def line():
        unit_num = yield number
        yield p.string(' units each with ')
        hp = yield number
        yield p.string(' hit points ')
        weaknesses, immunities = yield affinities.optional(([], []))
        yield p.string('with an attack that does ')
        dmg = yield number
        yield p.string(' ')
        dmg_type = yield word
        yield p.string(' damage at initiative ')
        initiative = yield number
        return Group(unit_num, hp, weaknesses, immunities, dmg, dmg_type, initiative)
    @p.generate
    def affinities():
        yield p.string('(')
        affinities = yield affinity.sep_by(p.string('; '), min=1)
        yield p.string(') ')
        weaknesses = []
        immunities = []
        for is_immunity, a in affinities:
            target = immunities if is_immunity else weaknesses
            for af in a:
                target.append(af)
        return weaknesses, immunities
    @p.generate
    def affinity():
        typ = yield p.string('weak') | p.string('immune')
        yield p.string(' to ')
        affinities = yield word.sep_by(p.string(', '))
        return typ == 'immune', affinities
    return file.parse(data)
