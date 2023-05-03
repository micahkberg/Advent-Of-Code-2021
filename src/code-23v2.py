"""
Revisiting this problem a year later. Going to start from
scratch with some different nomenclature and ideas.

input for part 1:
#############
#...........#
###B#C#A#D###
  #B#C#D#A#
  #########

input for part 2:
#############
#...........#
###B#C#A#D###
  #D#C#B#A#
  #D#B#A#C#
  #B#C#D#A#
  #########

"""

# strings defining layout
PART_1_INPUT = "#############" \
              "#...........#" \
              "###B#C#A#D###" \
              "  #B#C#D#A#" \
              "  ######### "

PART_2_INPUT = "#############" \
              "#...........#" \
              "###B#C#A#D###" \
              "  #D#C#B#A#" \
              "  #D#B#A#C#" \
              "  #B#C#D#A#" \
              "  #########"

# how much it costs to move the various species
energy_consumption = {"A": 1, "B": 10, "C": 100, "D": 1000}

# map of locations and how they are adjacent to other locations.
# i am only including locations where creatures could come to rest
# seemed just as easy to type it up as to automate lol
part_1_edges = {"A2": {"A1": 1}, "B2": {"B1": 1},
                "C2": {"C1": 1}, "D2": {"D1": 2},
                "A1": {"A2": 1, "L1": 2, "AB": 2},
                "B1": {"B2": 1, "AB": 2, "BC": 2},
                "C1": {"C2": 1, "BC": 2, "CD": 2},
                "D1": {"D2": 1, "CD": 2, "R1": 2},
                "L1": {"L2": 1, "AB": 2, "A1": 2},
                "R1": {"R2": 1, "CD": 2, "D1": 2},
                "L2": {"L1": 1}, "R2": {"R1": 1},
                "AB": {"A1": 2, "L1": 2, "B1": 2, "BC": 2},
                "BC": {"B1": 2, "AB": 2, "C1": 2, "CD": 2},
                "CD": {"C1": 2, "BC": 2, "D1": 2, "R1": 2}
                }


def make_init_position_dict(input_string, edges):
    """
    input_string: the string that represents starting conditions
    edges: hand typed representation of edges

    returns: filled out dictionary of item locations
    """
    locations = {i: None for i in edges}
    letters = "ABCD"
    row = 0
    col = 0
    for char in input_string:
        if char in letters:
            locations[letters[col] + str(row+1)] = char
            col += 1
            if col == 4:
                col = 0
                row += 1
    return locations


def path_between(arrangement, edges, p1, p2):
    dists = {p2: 9999999999}
    todo = []
    for n in edges[p1].keys():
        if not arrangement[n]:
            todo.append(n)
            dists[n] = edges[p1][n]
    while len(todo) > 0:
        n = todo.pop(0)
        for m in edges[n]:
            if not arrangement[m]:
                if m not in dists.keys():
                    dists[m] = dists[n]+edges[n][m]
                    todo.append(m)
                elif dists[n]+edges[n][m]<dists[m]:
                    dists[m] = dists[n] + edges[n][m]
    if dists[p2] == 9999999999:
        return False
    else:
        return dists[p2]*energy_consumption[arrangement[p1]]


def done_moving(arrangement, position):
    """
    checks if a given position is done moving and is in its final resting place
    """
    column = position[0]
    depth = position[1]
    resident = arrangement[position]
    if depth in letters or column != resident:
        return False
    for location in arrangement.keys():
        if location[0] == column and location[1] not in letters:
            if int(location[1]) > depth and arrangement[location] not in [None, column]:
                return False
    return True


def path_to_home(arrangement, position):
    # is home open?
    resident = arrangement[position]
    home_occupants = {}
    for location in arrangement.keys():
        if location[0] == resident and location[1] not in letters:
            home_occupants[location[1]] = arrangement[location]
    if home_occupants["1"]:
        return False
    if home_occupants["2"] in letters and home_occupants != resident:
        return False
    return True


def can_move(arrangement, position):
    resident = arrangement[position]
    if not resident:
        return False
    elif done_moving(arrangement, position):
        return False
    neighbors = part_1_edges[position]
    open_neighbors = []
    for neighbor in neighbors:
        if not arrangement[neighbor]:
            open_neighbors.append(neighbor)
    if len(open_neighbors)==0:
        return False
    in_hallway = not(position[0] in letters and position[1] not in letters)
    if in_hallway:
        return path_to_home(arrangement, position)


def main(part_num=1):
    if part_num == 1:
        input_string = PART_1_INPUT
        edges  = part_1_edges
    else:
        input_string = PART_2_INPUT
        # edges = PART_2_EDGES

    locations = make_init_position_dict(input_string, edges)


main(part_num=1)
