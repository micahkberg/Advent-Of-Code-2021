from load import openfile
import copy

today = "Day12"
lines = openfile(today+".txt")

class Cave:
    def __init__(self, name):
        self.name = name
        self.small = name[0].islower()
        self.neighbors = []

    def __repr__(self):
        return(f"<<{self.name}>>")

paths = []
caves = []
paths_2 = []
for line in lines:
    caveA, caveB = line.split("-")
    caveAfound = False
    caveBfound = False
    for cave in caves:
        if caveA == cave.name:
            caveAfound = True
            cave.neighbors.append(caveB)
        elif caveB==cave.name:
            caveBfound = True
            cave.neighbors.append(caveA)
    if not caveAfound:
        new_caveA = Cave(caveA)
        new_caveA.neighbors.append(caveB)
        caves.append(new_caveA)
        if caveA == "start":
            paths.append([new_caveA])
            paths_2.append([new_caveA])
    if not caveBfound:
        new_caveB = Cave(caveB)
        new_caveB.neighbors.append(caveA)
        caves.append(new_caveB)
        if caveB == "start":
            paths.append([new_caveB])
            paths_2.append([new_caveB])

def check_legality(cave_obj,path_list):
    if path_list[-1].name != "end":
        if path_list[-1].name in cave_obj.neighbors and (not cave_obj.small or cave_obj.name not in list(map(lambda i: i.name, path_list))):
            return True
        else:
            return False
    else:
        return False

print(list(map(lambda i: i.name, caves)))
Traversing = True
while Traversing:
    Traversing = False
    for cave in caves:
        new_paths = []
        for path in paths:
            if check_legality(cave,path):
                new_paths.append(path+[cave])
        if new_paths:
            for path in new_paths:
                if path not in paths:
                    paths.append(path)
                    Traversing = True
count = 0
for path in paths:
    if path[0].name == "start" and path[-1].name == "end":
        count+=1
print("answer 1")
print(count)

####################### part 2


def check_legality_2(cave_obj,path_list):
    if path_list[-1].name != "end" and cave_obj.name != "start" and path_list[-1].name in cave_obj.neighbors:
        # can't put start in list, don't sweat if its the end, and it has to be a neighbor
        if not cave_obj.small: # if its big: add it
            return True
        elif cave_obj.small and path_list.count(cave_obj) == 0: # small and there isn't 1 copy yet
            return True
        elif cave_obj.small and path_list.count(cave_obj) == 1: # otherwise if its small still, and there could be a 2nd
            doubles_already = False
            for step_cave in path_list:
                if step_cave.small and path_list.count(step_cave) == 2:
                    doubles_already = True
            if doubles_already:
                return False
            else:
                return True
        else:
            return False
    else:
        return False


Traversing = True
while Traversing:
    Traversing = False
    print(f"current count: {len(paths_2)}")
    new_paths = []
    for path in paths_2:
        if path[0].name == "start" and path[-1].name == "end":
            new_paths.append(path)
    for cave in caves:
        for path in paths_2:
            if check_legality_2(cave,path):
                new_paths.append(path+[cave])
                Traversing = True
    paths_2 = copy.copy(new_paths)
    #print(paths_2)

print("answer 2")
print(len(paths_2))
# print_list = list(map(lambda i: list(map(lambda j: j.name, i)), paths_2))
# print_list.sort()
# for line in print_list:
#     print(line)
