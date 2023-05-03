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

# types of creatures
LETTERS = "ABCD"

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
    row = 0
    col = 0
    for char in input_string:
        if char in LETTERS:
            locations[LETTERS[col] + str(row + 1)] = char
            col += 1
            if col == 4:
                col = 0
                row += 1
    return locations


def in_hallway(location):
    """ checks if a location code is in the upper hallway """
    if location[0] in LETTERS and location[1] in LETTERS:
        return True
    if location[0] in "LR":
        return True
    return False


class CaveSystem:
    """ class for holding data and funcs related to the system state """
    def __init__(self, edges, creature_dict):
        self.cave_map = edges
        self.creatures = creature_dict

    def at_home(self, point):
        """Looks at a point to see if its in its final resting place"""
        creature = self.creatures[point]
        col = point[0]
        depth = point[1]
        if not creature or col != creature or depth in LETTERS:
            # if the tile is empty OR
            # if col doesn't match creature OR
            # if the depth is actually ABCD (ie in hallway)
            # then not at rest
            return False
        home_spot_below = col + str(int(depth)+1)
        if home_spot_below not in self.cave_map:
            return True
        return self.at_home(home_spot_below)

    def system_complete(self):
        for node in self.creatures:
            if self.creatures[node]:
                if not self.at_home(node):
                    return False
        return True

    def is_destination_allowed(self, start_point, end_point):
        """ checks to see if creatures is allowed to move to the destination """
        if self.creatures[end_point]:
            return False
        if in_hallway(start_point) and in_hallway(end_point):
            return False
        if in_hallway(start_point):
            home_cave = self.creatures[start_point]
            if not(end_point[0] == home_cave and end_point[1] not in LETTERS):
                return False
        return True

    def is_path_between(self, start_point, end_point):
        """
        takes two points and determines the energy cost to move
        from point 1 to point 2, otherwise returns false if path
        is blocked by intermediary creatures or if the destination
        is not otherwise allowed.
        """
        # check destination
        if not self.is_destination_allowed(start_point, end_point):
            return False

        # initialize dictionary defining travel distances
        dists = {end_point: 999999999}
        todo = []
        for node in self.cave_map[start_point]:
            if not self.creatures[node]:
                todo.append(node)
                dists[node] = self.cave_map[start_point][node]
        while len(todo) > 0:
            x = todo.pop(0)
            for y in self.cave_map[x]:
                if not self.creatures[y]:
                    if y not in dists:
                        dists[y] = dists[x] + self.cave_map[x][y]
                        todo.append(y)
                    elif dists[x] + self.cave_map[x][y] < dists[y]:
                        dists[y] = dists[x] + self.cave_map[x][y]
        if dists[end_point] == 999999999:
            return False
        return dists[end_point]*energy_consumption[self.creatures[start_point]]


def main(part_num=1):
    """ main, part num alters which version of the problem is being solved """
    if part_num == 1:
        input_string = PART_1_INPUT
        edges = part_1_edges
    else:
        input_string = PART_2_INPUT
        # edges = PART_2_EDGES

    locations = make_init_position_dict(input_string, edges)
    start_cave = CaveSystem(edges, locations)
    cur_cave = start_cave
    while True:
        if cur_cave.system_complete():
            break



main(part_num=1)
