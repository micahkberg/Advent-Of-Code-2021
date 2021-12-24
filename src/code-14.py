from load import openfile

today = "Day14"
lines = openfile(today+".txt")

polymer = lines[0]
rules_raw = lines[2:]

rules = {}
for line in rules_raw:
    parts = line.split(" -> ")
    rules[parts[0]] = parts[1]

for step in range(10):

    new_polymer = ""
    for i in range(len(polymer)-1):
        pair = polymer[i:i+2]
        if pair in rules.keys():
            new_polymer += pair[0] + rules[pair]
    polymer = new_polymer + polymer[-1]


counts = {i: polymer.count(i) for i in set(polymer)}
print(counts)
print(2979-976)

current_pairs = {}
letter_counts = {}
for i in range(len(lines[0])-1):
    pair = lines[0][i:i+2]
    if pair in current_pairs.keys():
        current_pairs[pair] += 1
    else:
        current_pairs[pair] = 1
for char in lines[0]:
    if char in letter_counts.keys():
        letter_counts[char] += 1
    else:
        letter_counts[char] = 1

for step in range(40):
    next_pairs = {}
    for pair in current_pairs.keys():
        if pair in rules.keys():
            pairA = pair[0] + rules[pair]
            pairB = rules[pair] + pair[1]
            if rules[pair] in letter_counts.keys():
                letter_counts[rules[pair]] += current_pairs[pair]
            else:
                letter_counts[rules[pair]] = current_pairs[pair]

            for pairing in [pairA,pairB]:
                if pairing in next_pairs.keys():
                    next_pairs[pairing] += current_pairs[pair]
                else:
                    next_pairs[pairing] = current_pairs[pair]
        else:
            if pair in next_pairs.keys():
                next_pairs[pair] += current_pairs[pair]
            else:
                next_pairs[pair] = current_pairs[pair]
    current_pairs = next_pairs.copy()

print(max(letter_counts.values())-min(letter_counts.values()))
