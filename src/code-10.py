from load import openfile
import numpy as np
today = "Day10"
lines = openfile(today+".txt")

wrongers = []
fixes = []
matching = {
    "{":"}",
    "[":"]",
    "(":")",
    "<":">"
}

for line in lines:
    broken = False
    opened = []
    for char in line:
        if char in "({<[":
            opened.append(char)
        elif char in "}])>":
            if char == matching[opened[-1]]:
                opened = opened[:-1]
            else:
                wrongers.append(char)
                broken = True
                break

    if not broken:
        fix = []
        for char in opened[::-1]:
            fix.append(matching[char])
        fixes.append(fix)

score = 0
points = {")":3,
          "]":57,
          "}":1197,
          ">":25137}
for char in wrongers:
    score += points[char]
print(score)


score2 = []
points2 = {
    ")":1,
    "]":2,
    "}":3,
    ">":4
}
for fix in fixes:
    score_part = 0
    for char in fix:
        score_part *= 5
        score_part += points2[char]
    score2.append(score_part)
scores = sorted(score2)
print(scores[int(np.floor(len(scores)/2))])
