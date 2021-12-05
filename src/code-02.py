from load import openfile

today = "Day02"
lines = openfile(today+".txt")
print(lines)
directions = {
    "forward": [1,0],
    "down": [0,1],
    "up": [0,-1]
}

x = 0
y = 0


for line in lines:
    if line:
        dir, val = line.split()
        val = int(val)
        x += directions[dir][0]*val
        y += directions[dir][1]*val

print("answer 1")
print(x*y)


x = 0
y = 0
aim = 0
for line in lines:
    if line:
        dir, val = line.split()
        val = int(val)
        if dir == "forward":
            x += directions[dir][0]*val
            y += aim*val
        else:
            aim += directions[dir][1]*val
print("answer 2")
print(x*y)