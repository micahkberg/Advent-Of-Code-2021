from load import openfile

today = "Day07"
lines = openfile(today+".txt")
test = [16,1,2,0,4,2,7,1,2,14]
crabs = list(map(int, lines[0].split(',')))

#crabs = test

mn = min(crabs)
mx = max(crabs)
costs = list(range(mn, mx+1))
for i in range(len(costs)):
    costs[i] = sum(list(map(lambda j: abs(j-i), crabs)))
print(min(costs))

new_costs = list(range(mn, mx+1))


def move(crab, pos):
    distance = abs(crab-pos)
    gas = distance * (1 + distance) / 2
    return gas

for i in range(len(new_costs)):
    new_costs[i] = sum(list(map(lambda j: move(j,i), crabs)))
print(int(min(new_costs)))
print(new_costs)