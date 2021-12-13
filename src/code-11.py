from load import openfile
import itertools

today = "Day11"
lines = openfile(today+".txt")
lines = list(map(list, lines))
flashes = 0

class Octopus:
    def __init__(self, coord, energy):
        self.coord = coord
        self.x = self.coord[0]
        self.y = self.coord[1]
        self.energy = energy
        self.neighbors = self.get_neighbors()
        self.ready_to_flash = False
        self.flashed_this_step = False

    def grow(self):
        self.energy += 1
        if self.energy == 10:
            self.ready_to_flash = True

    def reset(self):
        self.flashed_this_step = False
        if self.energy >= 10:
            self.energy = 0

    def flash(self, octopus_list):
        global flashes
        flashes += 1
        for octo in octopus_list:
            if octo.coord in self.neighbors:
                octo.grow()
        self.ready_to_flash = False
        self.flashed_this_step = True

    def get_neighbors(self):
        adjs = list(itertools.product([1, 0, -1], [1, 0, -1]))
        adjs.remove((0, 0))
        neighbors = []
        for i in adjs:
            if self.x+i[0] in range(10) and self.y+i[1] in range(10):
                neighbors.append([x + i[0], y + i[1]])
        return neighbors


# make all octos
octos = []
for y in range(len(lines)):
    for x in range(len(lines[0])):
        octos.append(Octopus([x, y], int(lines[y][x])))


def step():
    for octo in octos:
        octo.grow()
    flashing = True
    while flashing:
        flashing = False
        for octo in octos:
            if octo.ready_to_flash:
                octo.flash(octos)
                flashing = True
    mega_flash = True
    for octo in octos:
        if not octo.flashed_this_step:
            mega_flash = False
            break
    if mega_flash:
        return True
    for octo in octos:
        octo.reset()
    return False


for k in range(1000):
    if step():
        print(k+1)
        break
print(flashes)




