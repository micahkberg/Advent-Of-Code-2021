from load import openfile
import numpy as np

today = "Day05"
lines = openfile(today+".txt")

data = []
for line in lines:
    parts = line.split(" -> ")
    arr = list(map(lambda i: i.split(","), parts))
    coords_int = [list(map(int, arr[0])), list(map(int, arr[1]))]
    data.append(coords_int)

def check_v_or_h(coords):
    if coords[0][0]==coords[1][0] or coords[0][1]==coords[1][1]:
        return True
    else:
        return False


def get_mag(vector):
    if vector[0] and vector[1]:
        return abs(vector[0])
    else:
        return abs(sum(vector))

def length(coords):
    vector = [coords[1][0]-coords[0][0], coords[1][1]-coords[0][1]]
    steps = []
    mag = get_mag(vector)
    for i in range(int(mag)+1): # only works for h or v lines
        steps.append([coords[0][0]+vector[0]*i/mag, coords[0][1]+vector[1]*i/mag])
    return(list(map(str, steps)))


danger_points = {}
for trench in data:
    if check_v_or_h(trench):
        for point in length(trench):
            if point in danger_points.keys():
                danger_points[point] += 1
            else:
                danger_points[point] = 1

ans = 0
for i in danger_points.keys():
    if danger_points[i]>1:
        ans+=1
print(f"Answer 1: {ans}")

ans2 = 0
complete_danger_points = {}
for trench in data:
    for point in length(trench):
        if point in complete_danger_points.keys():
            complete_danger_points[point] += 1
        else:
            complete_danger_points[point] = 1
for i in complete_danger_points.keys():
    if complete_danger_points[i]>1:
        ans2 += 1
print(f"Answer 2: {ans2}")