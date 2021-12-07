from load import openfile

today = "Day06"
lines = openfile(today+".txt")
import copy

fish_all = list(map(int, lines[0].split(",")))
fish_gens = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in fish_all:
    fish_gens[i] += 1
print(f"initialized... {fish_gens}")
for day in range(256):
    new_fish_gens = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    new_fish_gens[8] += fish_gens[0]

    for i in range(len(fish_gens)):
        next_gen = i - 1
        if next_gen == -1:
            next_gen = 6
        new_fish_gens[next_gen] += fish_gens[i]
    fish_gens = copy.deepcopy(new_fish_gens)
    if day == 79:
        print(f"Answer 1: {sum(fish_gens)}")


print(fish_gens)
print(f"Answer 2: {sum(fish_gens)}")