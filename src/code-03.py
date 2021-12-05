from load import openfile

import numpy as np

today = "Day03"
lines = openfile(today+".txt")
lines = list(map(list, lines))

data = np.array(lines[:-1])
data = data.astype('int8')

gamma = ""
for i in range(len(data[0])):
    gamma += str(round(np.average(data[:, i])))


epsilon = ""
for i in gamma:
    if i=="1":
        epsilon+="0"
    else:
        epsilon+="1"

def get_bin(bstring):
    val = 0
    for j in range(len(bstring)):
        dig_val = int(bstring[-(j+1)])*(2**(j))
        #print(dig_val)
        val+= dig_val
    return val
#print(gamma)
int_gamma = get_bin(gamma)
#print(epsilon)
int_epsilon = get_bin(epsilon)
#print(gamma)
#print(epsilon)
power = int_gamma * int_epsilon
print(f"Answer 1: {power}")

x_len = len(data[0])
y_len = len(data)


def bin_max(lis):
    avg = np.average(lis)
    if avg == 0.5:
        return 1
    else:
        return round(avg)


def bin_min(lis):
    return flip(bin_max(lis))


def flip(char):
    return 0 if char == 1 else 1


og_table = np.ones(len(data[:,0])) == 1
scrub_table = np.ones(len(data[:,0])) == 1
for i in range(x_len):
    og_slice = data[og_table][:,i]
    scrub_slice = data[scrub_table][:,i]

    print(f"The number of lines being considered for Oxygen: {len(og_slice)} and for scrubbing {len(scrub_slice)}")
    print(f"Oxy: {og_slice}")
    print(f"Scr: {scrub_slice}")
    if len(og_slice)==1:
        og_val = og_slice[0]
    else:
        og_val = bin_max(og_slice)
    if len(scrub_slice)==1:
        scrub_val = scrub_slice[0]
    else:
        scrub_val = bin_min(scrub_slice)

    print(f"Oxygen: {og_val}, Scrubbing: {scrub_val}")

    og_table *= data[:,i]==og_val
    scrub_table *= data[:,i]==scrub_val

print(data[og_table][0])
print(data[scrub_table][0])

og_rating = get_bin(data[og_table][0])
scrub_rating = get_bin(data[scrub_table][0])
print(og_rating)
print(scrub_rating)

ls_rating = og_rating * scrub_rating
print(ls_rating)
