import queue
from math import ceil

from load import openfile
import itertools

today = "Day23"
# puzzle input
# #############
# #...........#
# ###B#C#A#D###
#   #B#C#D#A#
#   #########

# numbering shcema
# #############
# #89.A.B.C.DE#
# ###0#2#4#6###
#   #1#3#5#7#
#   #########


begin_arrangement = tuple("BBCCADDA") + (None,)*7
final_arrangement = tuple("AABBCCDD") + (None,)*7
vertices = itertools.permutations(final_arrangement)

home_indices = {}
hall_pos = {"A":9.5,"B":10.5,"C":11.5,"D":12.5}

i = 0
for char in "ABCD":
    home_indices[char] = list(range(0+i*2,i*2+2))
    i+=1


def path_blocked(permutation, index, spot):
    if index<8:
        if spot<hall_pos[permutation[index]]:
            for check in range(spot,ceil(hall_pos[permutation[index]])):
                if permutation[check]:
                    return True
        else:
            for check in range(ceil(hall_pos[permutation[index]]),spot):
                if permutation[check]:
                    return True
    else:
        if hall_pos[spot]<index:
            for check in range(ceil(hall_pos[spot]),index):
                if permutation[check]:
                    return True
        else:
            for check in range(index,ceil(hall_pos[spot])):
                if permutation[check]:
                    return True

    return False

def get_new_positions(permutation):
    # permutation in format of list of None's and AABBCCDD's
    # for each index with a letter
    new_positions = []
    for index in range(len(permutation)):
        if permutation[index]: # for each not None char in permutation
            char = permutation[index]
            if index<8: # for the guys in the holes already
                if index%2==1 and permutation[index-1]: # trapped under another guy
                    continue
                new_spots = range(8,15)
                for spot in new_spots:
                    if not permutation[spot] and not path_blocked(permutation, index, spot):
                        new_position = list(permutation)
                        new_position[index] = None
                        new_position[spot]
            else: # for guys in hallways
                if not permutation[home_indices[permutation[index]][0]]:
                    pass


def dijkstra(graph, start_vertex):
    D = {} # if not in dict, is float(inf)
    Visited = []
    D[begin_arrangement] = 0
    pq = queue.PriorityQueue()
    pq.put((0, begin_arrangement))
    while not pq.empty():
        (dist, current_vertex) = pq.get()
        Visited.append(current_vertex)
        for position in get_new_positions(current_vertex):
            pass


dijkstra(vertices, begin_arrangement)
print("Finished")

path_blocked(begin_arrangement,0,12)

