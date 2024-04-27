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

def create_starting_forces():
    immune_system = Force([
        Group(2086, 11953, [], [], 46, 'cold', 13),
        Group(329, 3402, ['bludgeoning'], [], 90, 'slashing', 1),
        Group(414, 7103, ['bludgeoning'], ['radiation'], 170, 'radiation', 4),
        Group(2205, 7118, ['fire'], ['cold'], 26, 'radiation', 18),
        Group(234, 9284, ['slashing'], ['cold', 'fire'], 287, 'radiation', 12),
        Group(6460, 10804, ['fire'], [], 15, 'slashing', 11),
        Group(79, 1935, [], [], 244, 'radiation', 8),
        Group(919, 2403, ['fire'], [], 22, 'slashing', 2),
        Group(172, 1439, ['slashing'], ['cold', 'fire'], 69, 'slashing', 3),
        Group(1721, 2792, ['radiation', 'fire'], [], 13, 'cold', 16)
    ])

    infection = Force([
        Group(1721, 29925, ['cold', 'radiation'], ['slashing'], 34, 'radiation', 5),
        Group(6351, 21460, ['cold'], [], 6, 'slashing', 15),
        Group(958, 48155, ['bludgeoning'], [], 93, 'radiation', 7),
        Group(288, 41029, ['radiation'], ['bludgeoning'], 279, 'cold', 20),
        Group(3310, 38913, [], [], 21, 'radiation', 19),
        Group(3886, 16567, [], ['bludgeoning', 'cold'], 7, 'cold', 9),
        Group(39, 7078, [], [], 300, 'bludgeoning', 14),
        Group(241, 40635, ['cold'], [], 304, 'fire', 6),
        Group(7990, 7747, [], ['fire'], 1, 'radiation', 10),
        Group(80, 30196, ['fire'], [], 702, 'bludgeoning', 17)
    ])

    return (immune_system, infection)

def create_sample_forces():
    immune_system = Force([
        Group(17, 5390, ['radiation', 'bludgeoning'], [], 4507, 'fire', 2),
        Group(989, 1274, ['bludgeoning', 'slashing'], ['fire'], 25, 'slashing', 3)
    ])

    infection = Force([
        Group(801, 4706, ['radiation'], [], 116, 'bludgeoning', 1),
        Group(4485, 2961, ['fire', 'cold'], ['radiation'], 12, 'slashing', 4)
    ])

    return (immune_system, infection)
