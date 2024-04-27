data = '1113122113'

def look_and_say(inp: str):
    result = ''
    streak = 0
    character = ''
    for c in inp:
        if c != character and character != '':
            result += str(streak)
            result += character
            streak = 1
            character = c
        else:
            character = c
            streak += 1
    result += str(streak)
    result += character
    return result

# part 1
result = data
for i in range(40):
    result = look_and_say(result)

print(len(result))

# part 2
for i in range(10):
    result = look_and_say(result)

print(len(result))
