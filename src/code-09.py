from load import openfile
import numpy as np

today = "Day09"
lines = openfile(today+".txt")
heights = list(map(list, lines))
lim_x = list(range(len(lines[0])))
lim_y = list(range(len(lines)))

neighbors = [[0,1],[1,0],[-1,0],[0,-1]]


def get_neighbor_heights(x,y):
    targets = list(map(lambda coord: np.add(coord,[x,y]), neighbors))
    results = []
    for target in targets:
        if target[0] in lim_x and target[1] in lim_y:
            results.append(int(heights[target[1]][target[0]]))
    return results


def problem1():
    lows = []
    low_coords = []
    for i in lim_x:
        for j in lim_y:
            here = int(heights[j][i])
            others = sorted(get_neighbor_heights(i,j))
            if here < others[0]:
                lows.append(here)
                low_coords.append([i,j])
    print("Answer 1")
    print(sum(lows)+len(lows))
    return(low_coords)


def get_neighbor_coords(x,y):
    targets = list(map(lambda coord: list(np.add(coord,[x,y])), neighbors))
    results = []
    for target in targets:
        if target[0] in lim_x and target[1] in lim_y:
            results.append(target)
    return results


def problem2():
    lows = problem1()
    basin_sizes = []
    for low in lows:
        basin = [low]
        new_basin = [low]
        while True:
            new_neighbors = []
            for tile in new_basin:
                new_neighbors += get_neighbor_coords(tile[0],tile[1])
            finished = True
            new_basin = []
            for neighbor in new_neighbors:
                #print(neighbor)
                #print(basin)
                if not any(coord == neighbor for coord in basin) and heights[neighbor[1]][neighbor[0]] != '9':
                    basin.append(neighbor)
                    new_basin.append(neighbor)
                    finished = False
            if finished:
                break
        basin_sizes.append(len(basin))
    sorted_basins = sorted(basin_sizes)
    print(sorted_basins)
    print("Answer 2")
    print(sorted_basins[-1]*sorted_basins[-2]*sorted_basins[-3])

problem2()


