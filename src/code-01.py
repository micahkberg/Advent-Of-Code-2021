from load import openfile

today = "Day01"
lines = openfile(today+".txt")
lines = list(map(int, lines))

print(lines)
last_line = 100000
ans = 0
for line in lines:
    if int(line)>last_line:
        ans+=1
    last_line = int(line)
print(ans)

ans2 = 0
for i in range(len(lines)-3):
    if (sum(lines[i+1:i+4])>sum(lines[i:i+3])):
        ans2 += 1

print(ans2)

