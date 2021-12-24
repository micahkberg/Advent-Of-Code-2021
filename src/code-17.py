from load import openfile
import numpy as np

today = "Day17"
lines = openfile(today+".txt")[0]
print(lines)
x_range = range(209,238+1)
y_range = range(-86,-59+1)
reasonable_x_vals = list(range(1,300))

# test:
#x_range = range(20,30+1)
#y_range = range(-10,-5+1)

part_1 = (-min(y_range)-1)*((-min(y_range)-1)+1)/2
print(part_1)

possible_x_vals = []
for x in reasonable_x_vals:
    Pos = 0
    x_v = x
    step = 0
    while Pos < max(x_range)+1 and x_v != 0:
        step+=1
        if Pos in x_range:
            possible_x_vals.append(x)
            break
        Pos += x_v
        x_v = x_v-1 if x_v != 0 else 0

print(possible_x_vals)


def xsteps(x0,step):
    pos = 0
    x_v = x0
    for s in range(step):
        pos += x_v
        x_v = x_v-1 if x_v != 0 else 0
    return pos


reasonable_y_vals = range(min(y_range)-10,-min(y_range)+10)
print(reasonable_y_vals)
solutions = []
for y in reasonable_y_vals:
    step = 0
    pos = 0
    y_v = y
    while pos>min(y_range)-10:
        if pos in y_range:
            for x in reasonable_x_vals:
                if xsteps(x,step) in x_range and (x,y) not in solutions:
                    solutions.append((x,y))
        step+=1
        pos += y_v
        y_v -= 1
#not 1321
#not 1347

print(solutions)
print(len(solutions))
