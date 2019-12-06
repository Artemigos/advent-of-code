import common
from .data import *

def target_phase(immune_system, infection):
    power_list = list(sorted(immune_system.groups + infection.groups, key=lambda x: x.get_effective_power()*100+x.initiative, reverse=True))
    result = {}

    for group in power_list:
        enemies = infection.groups if group in immune_system.groups else immune_system.groups
        max_damage = 0
        max_enemy = None
        for enemy in enemies:
            if enemy in result.values() or enemy.is_dead():
                continue
            damage = enemy.calculate_received_damage(group)
            if max_enemy is None:
                max_enemy = enemy
                max_damage = damage
                continue
            if damage > max_damage or \
                    (damage == max_damage and enemy.get_effective_power() > max_enemy.get_effective_power()) or \
                    (damage == max_damage and enemy.get_effective_power() == max_enemy.get_effective_power() and enemy.initiative > max_enemy.initiative):
                max_enemy = enemy
                max_damage = damage
        if max_damage > 0:
            result[group] = max_enemy

    return result

def attack_phase(immune_system, infection, target_info):
    # report status
    print("Immune System:")
    for i, group in enumerate(immune_system.groups):
        if not group.is_dead():
            print(f"Group {i+1} contains {group.units} units")
    print("Infection:")
    for i, group in enumerate(infection.groups):
        if not group.is_dead():
            print(f"Group {i+1} contains {group.units} units")
    print()

    # perform attacks
    for group in sorted(target_info.keys(), key=lambda x: x.initiative, reverse=True):
        enemy = target_info[group]
        killed = enemy.take_damage(group)
        print(f"{'Infection' if group in infection.groups else 'Immune System'} group {infection.groups.index(group)+1 if group in infection.groups else immune_system.groups.index(group)+1} attacks defending group {infection.groups.index(enemy)+1 if enemy in infection.groups else immune_system.groups.index(enemy)+1}, killing {killed} units")

    print('---')

def run_combat(immune_system_boost=0):
    (ImmuneSystem, Infection) = create_starting_forces()

    for group in ImmuneSystem.groups:
        group.damage += immune_system_boost

    while not ImmuneSystem.is_dead() and not Infection.is_dead():
        target_info = target_phase(ImmuneSystem, Infection)
        attack_phase(ImmuneSystem, Infection, target_info)

    return (ImmuneSystem, Infection)

def print_solution(ImmuneSystem, Infection, label):
    units1 = sum(map(lambda x: x.units, ImmuneSystem.groups))
    units2 = sum(map(lambda x: x.units, Infection.groups))
    print(label, str(max(units1, units2)))

# part 1
ImmuneSystem, Infection = run_combat()
print_solution(ImmuneSystem, Infection, 'part 1:')

# part 2
ImmuneSystem, Infection = run_combat(38) # found with manual binary search
print_solution(ImmuneSystem, Infection, 'part 2:')
