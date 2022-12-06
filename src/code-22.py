from load import openfile

today = "Day22"
lines = openfile(today+".txt")

total_on = 0

def cap_zone(coords):
    new_coord = [0,0]
    if coords[0]<-50:
        new_coord[0]=-50
    else:
        new_coord[0]=coords[0]
    if coords[1]>50:
        new_coord[1]=50
    else:
        new_coord[1]=coords[1]
    return new_coord

def do_instruction(instruction, cubes):
    switch_to, zones = instruction.split(" ")
    zones = list(map(lambda i: list(map(int, i.split(".."))), list(map(lambda i: i[2:], zones.split(",")))))
    x, y, z = zones
    xs = cap_zone(x)
    ys = cap_zone(y)
    zs = cap_zone(z)
    for x in range(xs[0],xs[1]+1):
        for y in range(ys[0],ys[1]+1):
            for z in range(zs[0],zs[1]+1):
                if switch_to == "on":
                    cubes.add((x,y,z))
                elif switch_to == "off" and (x,y,z) in cubes:
                    cubes.remove((x,y,z))
    #print(len(cubes))


cubes = set()

for line in lines:
    if line:
        do_instruction(line, cubes)
# part 1: 648023

#################################################################################################


def overlapping_sector(sector1,sector2):
    xi = max([sector1.xi, sector2.xi])
    xf = min([sector1.xf, sector2.xf])
    yi = max([sector1.yi, sector2.yi])
    yf = min([sector1.yf, sector2.yf])
    zi = max([sector1.zi, sector2.zi])
    zf = min([sector1.zf, sector2.zf])
    if xi<=xf and yi<=yf and zi<=zf:
        return Cuboid([[xi, xf], [yi, yf], [zi, zf]], -sector2.value)
    else:
        return None


class Cuboid:
    def __init__(self, zones, value):
        self.xi, self.xf = zones[0]
        self.yi, self.yf = zones[1]
        self.zi, self.zf = zones[2]
        self.xrange = [self.xi, self.xf]
        self.yrange = [self.yi, self.yf]
        self.zrange = [self.zi, self.zf]
        self.ranges = [self.xrange,self.yrange,self.zrange]
        self.value = value #+1/-1



    def intersection(self,other_sector):
        sub_cube = overlapping_sector(self, other_sector)
        return sub_cube

    def volume(self):
        return self.value * (self.zf-self.zi + 1) * (self.yf - self.yi + 1) * (self.xf - self.xi + 1)




def part2():
    initial_cuboids = []
    final_cuboids = []
    for line in lines:
        value, zones = line.split(" ")
        value = 1 if value=="on" else -1
        zones = list(map(lambda i: list(map(int, i.split(".."))), list(map(lambda i: i[2:], zones.split(",")))))
        initial_cuboids.append(Cuboid(zones, value))

    for cuboid in initial_cuboids:
        new_cuboids = []
        if cuboid.value == 1:
            new_cuboids.append(cuboid)
        for sector in final_cuboids:
            intersection = cuboid.intersection(sector)
            if intersection:
                new_cuboids.append(intersection)
        final_cuboids += new_cuboids

    answer2 = 0
    for cuboid in final_cuboids:
        answer2 += cuboid.volume()
    print(f"part 2 answer: {answer2}")

# try 1: 1524454749374119 too high
# try 2: 1285677377848549
part2()
