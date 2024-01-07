from abc import abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Any

import common

lines = common.read_file().splitlines()

@dataclass
class Module:
    type: str
    name: str
    inputs: list[str]
    outputs: list[str]

# read module info
modules = {}
for line in lines:
    left, right = line.split(' -> ')
    typ, name = (left[0], left[1:]) if left != 'broadcaster' else (left, left)
    module = Module(typ, name, [], [])
    for tname in right.split(', '):
        module.outputs.append(tname)
    modules[name] = module

# build input list for all modules
for name in list(modules.keys()):
    module = modules[name]
    for output in module.outputs:
        target = modules.get(output)
        if target is None:
            target = Module('', output, [], [])
            modules[output] = target
        target.inputs.append(name)

# set up initial states
states: dict[str, Any] = {}
for name in modules:
    module = modules[name]
    if module.type == '%':
        states[name] = False
    elif module.type == '&':
        states[name] = {i: False for i in module.inputs}

# part 1
low_pulses, high_pulses = 0, 0
for _ in range(1000):
    q: deque[tuple[str, str, bool]] = deque()
    q.append(('button', 'broadcaster', False))
    while len(q) > 0:
        fro, to, high = q.popleft()
        # print(fro, '-high->' if high else '-low->', to)
        if high:
            high_pulses += 1
        else:
            low_pulses += 1
        module = modules[to]
        if module.type == 'broadcaster':
            for output in module.outputs:
                q.append((to, output, high))
        elif module.type == '%':
            if not high:
                new_state = states[to] = not states[to]
                for output in module.outputs:
                    q.append((to, output, new_state))
        elif module.type == '&':
            state: dict[str, bool] = states[to]
            state[fro] = high
            new_pulse = not all(state.values())
            for output in module.outputs:
                q.append((to, output, new_pulse))

print(low_pulses*high_pulses)

# part 2
def part2() -> int:
    class Mod:
        def __init__(self, name: str):
            self.outputs: 'list[Mod]' = []
            self.name = name
        @abstractmethod
        def add_pulses(self, fro: 'Mod', inp: bool, q: 'deque[tuple[Mod, Mod, bool]]'):
            ...
    class Dummy(Mod):
        def add_pulses(self, fro: 'Mod', inp: bool, q: 'deque[tuple[Mod, Mod, bool]]'):
            ...
    class Broadcaster(Mod):
        def add_pulses(self, fro: 'Mod', inp: bool, q: 'deque[tuple[Mod, Mod, bool]]'):
            for o in self.outputs:
                q.append((self, o, inp))
    class FlipFlop(Mod):
        def __init__(self, name: str):
            super(FlipFlop, self).__init__(name)
            self.state = False
        def add_pulses(self, fro: 'Mod', inp: bool, q: 'deque[tuple[Mod, Mod, bool]]'):
            if inp:
                return
            self.state = not self.state
            for o in self.outputs:
                q.append((self, o, self.state))
    class Conjunction(Mod):
        def __init__(self, name: str, inputs: list[str]):
            super(Conjunction, self).__init__(name)
            self.inputs = {i: False for i in inputs}
        def add_pulses(self, fro: Mod, inp: bool, q: 'deque[tuple[Mod, Mod, bool]]'):
            self.inputs[fro.name] = inp
            out = not all(self.inputs.values())
            for o in self.outputs:
                q.append((self, o, out))

    mods: dict[str, Mod] = {}
    for name in modules:
        module: Module = modules[name]
        if module.type == 'broadcaster':
            mods[module.name] = Broadcaster(module.name)
        elif module.type == '%':
            mods[module.name] = FlipFlop(module.name)
        elif module.type == '&':
            mods[module.name] = Conjunction(module.name, module.inputs)
        else:
            mods[module.name] = Dummy(module.name)

    for name in modules:
        module = modules[name]
        mod = mods[name]
        for output in module.outputs:
            mod.outputs.append(mods[output])
        if type(mod) is Conjunction:
            for inp in module.inputs:
                mod.inputs[inp] = False

    found_rx = False
    button_presses = 0
    while not found_rx:
        button_presses += 1
        print(button_presses, end='\r')
        q: deque[tuple[Mod, Mod, bool]] = deque()
        q.append((Dummy('button'), mods['broadcaster'], False))
        while len(q) > 0:
            fro, to, high = q.popleft()
            if not high and to.name == 'rx':
                found_rx = True
                break
            to.add_pulses(fro, high, q)

    return 0

print(part2())

# # reset states
# states = {}
# for name in modules:
#     module = modules[name]
#     if module.type == '%':
#         states[name] = False
#     elif module.type == '&':
#         states[name] = {i: False for i in module.inputs}
#
# # part 2
# found_rx = False
# button_presses = 0
# while not found_rx:
#     button_presses += 1
#     print(button_presses, end='\r')
#     q = deque()
#     q.append(('button', 'broadcaster', False))
#     while len(q) > 0:
#         fro, to, high = q.popleft()
#         if not high and to == 'rx':
#             found_rx = True
#             break
#         module = modules[to]
#         if module.type == 'broadcaster':
#             for output in module.outputs:
#                 q.append((to, output, high))
#         elif module.type == '%':
#             if not high:
#                 new_state = states[to] = not states[to]
#                 for output in module.outputs:
#                     q.append((to, output, new_state))
#         elif module.type == '&':
#             state = states[to]
#             state[fro] = high
#             new_pulse = not all(state.values())
#             for output in module.outputs:
#                 q.append((to, output, new_pulse))
#
# print()
# print(button_presses)
