import common
from .solution2 import run
Runtime = common.import_solution(2017, 18).Runtime


class RuntimeEx(Runtime):
    def __init__(self, instructions):
        super().__init__(instructions)
        self.mul_amount = 0

    def sub(self, reg, val):
        self.ensure_reg(reg)
        val = self.find_val(val)
        self.registers[reg] -= val
        self.instruction += 1

    def jnz(self, cmp, val):
        self.conditional_jump(lambda x: x != 0, cmp, val)

    def process_instr(self, instr=None):
        instr = instr or self.current_instruction()
        code = instr[0]
        if code == 'sub':
            self.sub(instr[1], instr[2])
        elif code == 'jnz':
            self.jnz(instr[1], instr[2])
        else:
            if code == 'mul':
                self.mul_amount += 1
            super().process_instr(instr)


def main():
    data = common.read_file()
    lines = data.splitlines()
    instructions = list(map(lambda x: x.split(' '), lines))

    rt = RuntimeEx(instructions)
    while True:
        rt.process_instr()
        if rt.instruction_out_of_bounds():
            break

    print(rt.mul_amount)


main()
run()
