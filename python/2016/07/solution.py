import itertools
import operator
import common

lines = common.read_file('2016/07/data.txt').splitlines()
# lines = [
#     'abba[mnop]qrst',
#     'abcd[bddb]xyyx',
#     'aaaa[qwer]tyui',
#     'ioxxoj[asdfgh]zxcvbn'
# ]

support_tls = 0
support_ssl = 0
for l in lines:
    segments = list(common.flat_map(lambda x: x.split('['), l.split(']')))

    # part 1
    found_outside = False
    found_inside = False
    for i, s in enumerate(segments):
        if i%2 == 0: # outside
            if found_outside:
                continue
            else:
                for j in range(0, len(s)-3):
                    if s[j] != s[j+1] and s[j] == s[j+3] and s[j+1] == s[j+2]:
                        found_outside = True
                        break
        else: # inside
            for j in range(0, len(s)-3):
                if s[j] != s[j+1] and s[j] == s[j+3] and s[j+1] == s[j+2]:
                    found_inside = True
                    break

        if found_inside:
            break
        
    if found_outside and not found_inside:
        support_tls += 1

    # part 2
    abas = []
    for i in range(0, len(segments), 2): # outsite
        s = segments[i]
        for j in range(0, len(s)-2):
            if s[j] == s[j+2] and s[j] != s[j+1]:
                abas.append(s[j:j+3])

    found_bab = False
    babs = list(map(lambda x: x[1]+x[0]+x[1], abas))
    for i in range(1, len(segments), 2): # inside
        s = segments[i]
        for j in range(0, len(s)-2):
            if s[j:j+3] in babs:
                found_bab = True
                break
        if found_bab:
            support_ssl += 1
            break

print(support_tls)
print(support_ssl)
