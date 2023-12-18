import common

data = common.read_file('2017/4/data.txt')
passphrases = common.split_table(data, ' ')


# part 1
def is_valid1(pp: list):
    return len(pp) == len(set(pp))


valid_passphrases = list(filter(is_valid1, passphrases))
print(len(valid_passphrases))


# part 2
def is_anagram(p1, p2):
    return sorted(p1) == sorted(p2)


def is_valid2(pp: list):
    if len(pp) != len(set(pp)):
        return False
    for i in range(len(pp)):
        for j in range(len(pp)):
            if i != j and is_anagram(pp[i], pp[j]):
                return False
    return True


valid_passphrases = list(filter(is_valid2, passphrases))
print(len(valid_passphrases))
