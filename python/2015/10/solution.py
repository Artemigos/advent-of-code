from dataclasses import dataclass
import common

data = common.read_file().strip()
nums = [ord(x) - ord('0') for x in data]

@dataclass
class Repeat:
    num: int
    amount: int

    def try_push(self, num: int, amount: int) -> bool:
        if num != self.num:
            return False
        self.amount += amount
        return True

def push(repeats: list[Repeat], num: int, amount: int):
    if len(repeats) == 0 or not repeats[-1].try_push(num, amount):
        repeats.append(Repeat(num, amount))

def r_len(repeats: list[Repeat]) -> int:
    return sum((x.amount for x in repeats))

repeats = []
for n in nums:
    push(repeats, n, 1)

def look_and_say(repeats: list[Repeat]) -> list[Repeat]:
    result = []
    for r in repeats:
        push(result, r.amount, 1)
        push(result, r.num, 1)
    return result

for _ in range(40):
    repeats = look_and_say(repeats)

print(r_len(repeats))

for _ in range(10):
    repeats = look_and_say(repeats)

print(r_len(repeats))
