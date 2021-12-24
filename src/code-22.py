from load import openfile

today = "Day22"
lines = openfile(today+".txt")

cubes = []
total_on = 0

def vol(x,y,z):
    return (1 + x[1] - x[0]) * (1 + y[1] - y[0]) * (1 + z[1] - z[0])

def do_instruction(instruction):
    switch_to, zones = instruction.split(" ")
    zones = list(map(lambda i: list(map(int, i.split(".."))), list(map(lambda i: i[2:], zones.split(",")))))
    x, y, z = zones
    new_cube = (((x[0],x[1]+1),(y[0],y[1]+1),(z[0],z[1]+1)), switch_to)
    volume = vol(x, y, z)
    if switch_to == "on":
        global total_on
        total_on += volume
    for cube,was in cubes:
        a, b, c = cube
        overlap = max(min(a[1],x[1])-max(a[0], x[0]), 0)*\
        max(min(b[1],y[1]) - max(b[0], y[0]), 0)*\
        max(min(c[0],z[0]) - max(c[0], z[0]), 0)
        if was=="on" and switch_to=="on":
            pass

    cubes.append(new_cube)





p=0
for line in lines:
    if line:
        p+=1
        do_instruction(line)
