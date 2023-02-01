"""
Revisting this problem a year later. Going to start from scratch with some different nomenclature and ideas.

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

part_1_input ="#############" \
              "#...........#" \
              "###B#C#A#D###" \
              "  #B#C#D#A#" \
              "  ######### "

part_2_input ="#############" \
              "#...........#" \
              "###B#C#A#D###" \
              "  #D#C#B#A#" \
              "  #D#B#A#C#" \
              "  #B#C#D#A#" \
              "  #########"

energy_consumption = {"A": 1, "B": 10, "C": 100, "D": 1000}

# map of locations and how they are adjacent to other locations.
# i am only including locations where creatures could come to rest
# seemed just as easy to type it up as to automate lol
part_1_edges = {"A2": {"A1": 1}, "B2": {"B1": 1},
                "A1": {"A2": 1, "L1": 2, "AB": 2},
                "B1": {"B2": 1, "AB": 2, "BC": 2},
                "C2": {"C1": 1}, "D2": {"D1": 2},
                "C1": {"C2": 1, "BC": 2, "CD": 2},
                "D1": {"D2": 1, "CD": 2, "R1": 2},
                "L1": {"L2": 1, "AB": 2, "A1": 2},
                "L2": {"L1": 1}, "R2": {"R1": 1},
                "R1": {"R2": 1, "CD": 2, "D1": 2},
                }

part_1_locations = {i: None for i in part_1_edges.keys()}

letters = "ABCD"
num = "1"
letter_i = 0
for char in part_1_input:
    if char in letters:
        part_1_locations[letters[letter_i] + num] = char
        letter_i = (letter_i+1) % 4
        if letter_i == 0:
            num = "2"



