from load import openfile

today = "Day25"
lines = openfile(today+".txt")
lines = lines[:-1]

for line in lines:
    print(line)

grid = {}
for x in range(len(lines[0])):
    for y in range(len(lines)):
        grid[(x, y)] = "."

def print_grid():
    out = ""
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            out+=str(grid[(x,y)])
        out+="\n"
    print(out)

class Cucumber:
    def __init__(self, pos, species):
        self.x, self.y = pos
        self.species = species
        self.moving = False

    def __str__(self):
        return self.species

    def check_viewpoint(self):
        if self.species == ">":
            if type(grid[((self.x+1)%len(lines[0]), self.y)]) == str:
                self.moving = ((self.x+1)%len(lines[0]), self.y)
        else:
            if type(grid[(self.x, (self.y+1)%len(lines))]) == str:
                self.moving = (self.x, (self.y+1)%len(lines))

    def move(self):
        if self.moving:
            grid[(self.x,self.y)] = "."
            grid[self.moving] = self
            self.x, self.y = self.moving
            self.moving = False
            return 1
        else:
            return 0

# initialize:

for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] != ".":
            grid[(x, y)] = Cucumber((x, y), lines[y][x])

steps = 0
cucumbers_that_moved = 999
while cucumbers_that_moved>0:
    steps+=1
    cucumbers_that_moved=0
    # move east
    for key in grid.keys():
        if grid[key] != ".":
            if grid[key].species == ">":
                grid[key].check_viewpoint()

    for key in grid.keys():
        if grid[key] != ".":
            if grid[key].species == ">":
                cucumbers_that_moved += grid[key].move()
    # move south
    for key in grid.keys():
        if grid[key] != ".":
            if grid[key].species == "v":
                grid[key].check_viewpoint()
    for key in grid.keys():
        if grid[key] != ".":
            if grid[key].species == "v":
                cucumbers_that_moved += grid[key].move()
    print(f"step {steps}: movement = {cucumbers_that_moved}")
    #tprint_grid()

#try1 = step27