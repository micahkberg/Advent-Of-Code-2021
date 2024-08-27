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

import itertools

# strings defining layout
PART_1_INPUT = "BCAD" \
               "BCDA"

PART_2_INPUT = "BCAD" \
               "DCBA" \
               "DBAC" \
               "BCDA"

TEST_INPUT = "BCBDADCA"

PART=2

# how much it costs to move the various species
energy_consumption = {"A": 1, "B": 10, "C": 100, "D": 1000}

# types of creatures
LETTERS = "ABCD"

# map of locations and how they are adjacent to other locations.
# i am only including locations where creatures could come to rest
# seemed just as easy to type it up as to automate lol
part_1_edges = {"A2": {"A1": 1}, "B2": {"B1": 1},
                "C2": {"C1": 1}, "D2": {"D1": 1},
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

part_2_edges = {"A2": {"A3": 1,"A1": 1}, "B2": {"B3": 1,"B1": 1},
                "C2": {"C3": 1,"C1": 1}, "D2": {"D3": 1,"D1": 1},
                "A3": {"A4": 1,"A2": 1}, "B3": {"B4": 1,"B2": 1},
                "C3": {"C4": 1,"C2": 1}, "D3": {"D2": 1,"D4": 1},
                "A4": {"A3": 1}, "B4": {"B3": 1},
                "C4": {"C3": 1}, "D4": {"D3": 1},
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


def cave_hash(cave_obj):
    return str(cave_obj)


def make_init_position_dict(input_string, edges):
    """
    input_string: the string that represents starting conditions
    edges: hand typed representation of edges

    returns: filled out dictionary of item locations
    """
    locations = {i: None for i in edges}
    row = 1
    col = 0
    for char in input_string:
        locations[LETTERS[col] + str(row)] = char
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
    def __init__(self, edges, tiles, energy_spent=0):
        self.edges = edges
        self.tiles = tiles
        self.energy_spent = energy_spent

    def __str__(self):
        to_fill_in_1 = "#############\n#12.3.4.5.67#\n###8#9#E#F###\n  #G#H#I#J#\n  #########"
        to_fill_in_2 = "#############\n#12.3.4.5.67#\n###8#9#E#F###\n  #G#H#I#J#\n    #K#L#M#N#\n  #O#P#Q#R#\n#########"
        if PART==1:
            printout = to_fill_in_1
        else:
            printout = to_fill_in_2
        keys = "123456789EFGHIJKLMNOPQR"
        locations = ['L2', 'L1', 'AB', 'BC', 'CD', 'R1', 'R2', 'A1', 'B1', 'C1', 'D1', 'A2', 'B2', 'C2', 'D2', 'A3', 'B3', 'C3', 'D3', 'A4', 'B4', 'C4', 'D4']
        for i in range(0, 15 if PART==1 else 23):
            char = self.tiles[locations[i]] if self.tiles[locations[i]] else '.'
            printout = printout.replace(keys[i], char)
        return printout

    def at_home(self, point):
        """Looks at a point to see if its in its final resting place"""
        creature = self.tiles[point] # gets the contents of a given tile
        if not creature:
            # if the tile is empty
            return False
        col = point[0]
        depth = point[1]
        if col != creature or depth in LETTERS:
            # if col doesn't match creature OR
            # if the depth is actually ABCD (ie in hallway)
            # then not at rest
            return False
        home_spot_below = col + str(int(depth)+1)
        if home_spot_below not in self.edges:
            return True
        return self.at_home(home_spot_below)

    def system_complete(self):
        for node in ["A1", "B1", "C1", "D1"]:
            # check all the top nodes, since the top ones also check below them
            if not self.at_home(node):
                return False
        return True

    def is_move_home(self, start_point, end_point):
        if in_hallway(end_point):
            return False
        destination_col = end_point[0]
        species = self.tiles[start_point]
        return destination_col == species

    def is_destination_allowed(self, start_point, end_point):
        """ checks to see if creatures is allowed to move to the destination """
        species = self.tiles[start_point]  # get the creature
        if self.tiles[end_point]:
            # is there something at the destination
            return False
        if in_hallway(start_point) and in_hallway(end_point):
            # are both these points hallways?
            return False
        if in_hallway(start_point):
            # if we are in hallway, have to be moving into our shaft
            if not(end_point[0] == species and end_point[1] not in LETTERS):
                # make sure destination is in a tile in their shaft
                return False
        if not in_hallway(end_point):
            # if endpoint is in a cave, has to be our home
            if end_point[0] != species:
                return False
        if end_point[0] == species and end_point[1] not in LETTERS:
            # if its moving home
            depth = int(end_point[1])
            for i in range(depth+1, PART*2+1):
                # walk thru each spot below
                spot_below = end_point[0]+str(i)
                if self.tiles[spot_below]:
                    # if inhabited
                    if self.tiles[spot_below] != species:
                        # if at home
                        return False
                else:
                    # if not inhabited
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
        dists = {start_point: 0, end_point: 999999999}
        todo = [start_point]
        while len(todo) > 0:
            cur_node = todo.pop(0)
            for next_node in self.edges[cur_node]:
                if not self.tiles[next_node]: # make sure path clear
                    if next_node not in dists:
                        dists[next_node] = dists[cur_node] + self.edges[cur_node][next_node]
                        todo.append(next_node)
                if next_node == end_point:
                    dists[end_point] = dists[cur_node] + self.edges[cur_node][next_node]
                    break
            if dists[end_point] < 999999999:
                break
        if dists[end_point] == 999999999:
            return False
        return dists[end_point]*energy_consumption[self.tiles[start_point]]

    def find_next_positions(self):
        new_positions = []
        empty = []
        guys = []
        for node in self.tiles:
            if self.tiles[node]:
                if not self.at_home(node):
                    guys.append(node)
            else:
                empty.append(node)
        for start, end in itertools.product(guys, empty):
            cost = self.is_path_between(start, end)
            if cost:
                creature = self.tiles[start]
                new_map = self.tiles.copy()
                new_map[start] = None
                new_map[end] = creature
                new_cave = CaveSystem(self.edges, new_map, self.energy_spent+cost)
                if self.is_move_home(start, end):
                    # if this is a move to a home column, its the most efficient move
                    # (or one of equally efficient moves)
                    # and so we don't have to compile the other moves
                    #print("moving a guy home")
                    #print("from")
                    #print(self)
                    #print("to")
                    #print(new_cave)
                    return [new_cave]
                new_positions.append(new_cave)
        return new_positions


def main(part_num=1):
    """ main, part num alters which version of the problem is being solved """
    if part_num == 1:
        input_string = PART_1_INPUT
        edges = part_1_edges
    else:
        input_string = PART_2_INPUT
        edges = part_2_edges
    #input_string = TEST_INPUT

    locations = make_init_position_dict(input_string, edges)
    start_cave = CaveSystem(edges, locations)
    caves = [start_cave]
    min_cost = 99999999999
    min_cost_of_state = {cave_hash(start_cave): 0}
    check_in_counter = 0
    while len(caves)>0:
        #caves = sorted(caves, key=lambda i: i.energy_spent)
        cur_cave = caves.pop(0)
        check_in_counter += 1
        if check_in_counter%1000==0:
            print(f"current number of states={len(caves)}")
            print(f"states visited = {len(min_cost_of_state)}")
            print(f"percentage of states visited:{str(2*100*len(min_cost_of_state)/(15*14*13*12*11*10*9*8))[:4]}%")
            print(f"=====================================")
        new_states = cur_cave.find_next_positions()
        for new_state in new_states:
            if new_state.energy_spent > min_cost:
                continue
            if new_state.system_complete():
                min_cost = min(min_cost, new_state.energy_spent)
                print(f"found routes with min cost {min_cost}")
            elif cave_hash(new_state) not in min_cost_of_state:
                min_cost_of_state[cave_hash(new_state)] = new_state.energy_spent
                caves.append(new_state)
            elif min_cost_of_state[cave_hash(new_state)] > new_state.energy_spent:
                min_cost_of_state[cave_hash(new_state)] = new_state.energy_spent
                caves.append(new_state)
        #if len(new_states)==0:
            #print(cur_cave)
    print(f"final resulting energy = {min_cost}")


main(part_num=PART)
