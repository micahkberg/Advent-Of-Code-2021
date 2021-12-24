from load import openfile
import json
import numpy as np
today = "Day18"
lines = openfile(today+".txt")

def snailadd(x,y):
    #print("adding...")
    return snailreduced([x,y])

def snailmagnitude(item):
    if type(item[0]) != list:
        L = item[0]
    else:
        L = snailmagnitude(item[0])
    if type(item[1]) != list:
        R = item[1]
    else:
        R = snailmagnitude(item[1])
    return (L*3)+(R*2)

def snailreduced(pair):
    #print("reducing...")
    reduced = False
    while not reduced:
        reduced = True
        if depth(pair)>4:
            #print("exceeds depth")
            #print(f"exploding...{pair}")
            pair = explode(pair)
            #print(f"exploded... {pair}")
            reduced = False
        elif maxsize(pair)>=10:
            #print("check maxsize")
            #print(f"pre-split {pair}")
            pair, cr = pairsplit(pair)
            #print(f"post-split {pair}")
            reduced = False
    return pair

def depth(item):
    if type(item) != list:
        return 0
    else:
        return max(depth(i) for i in item) + 1

def maxsize(item):
    if type(item) != list:
        return item
    else:
        return max(maxsize(i) for i in item)

def check_edge(d, idx_list):
    return (d == -1 and idx_list == len(idx_list) * [0]) or (d == 1 and idx_list == len(idx_list) * [1])

def get_next(direction, eq_line,idx_list):
    target_idx_list = idx_list.copy()
    sub_list = eq_line.copy()
    while not check_edge(direction,target_idx_list):
        pos_num = 0
        for i in range(1,len(target_idx_list)+1):
            pos_num += target_idx_list[-i]*(2**(i-1))
        pos_num += direction
        target_idx_list = list(map(int,list(str(bin(pos_num))[2:])))
        modf = [1] if direction == -1 else [0]
        target_idx_list = [0]*(4-len(target_idx_list)) + target_idx_list + modf+modf+modf
        sub_list = eq_line.copy()
        result = []
        for j in target_idx_list:
            result.append(j)
            sub_list = sub_list[j]
            if type(sub_list) != list:
                break
        if type(sub_list) != list:
            break

    if type(sub_list) != list:
        return result
    else:
        return None


def explode(pair):
    sublist = pair.copy()
    d=1
    idx_list = []
    while type(sublist[0])==list or type(sublist[1])==list:
        idx = 0
        for i in sublist:
            if depth(i) > 4-d:
                sublist = i
                d+=1
                idx_list.append(idx)
                break
            idx+=1
    lv = sublist[0]
    rv = sublist[1]

    next_l = get_next(-1,pair,idx_list)
    next_r = get_next(1,pair,idx_list)

    for i,addend in [[next_l,lv],[next_r,rv]]:
        if i:
            if len(i) == 1:
                pair[i[0]] += addend
            elif len(i) == 2:
                pair[i[0]][i[1]] += addend
            elif len(i) == 3:
                pair[i[0]][i[1]][i[2]] += addend
            elif len(i) == 4:
                pair[i[0]][i[1]][i[2]][i[3]] += addend
            elif len(i) == 5:
                pair[i[0]][i[1]][i[2]][i[3]][i[4]] += addend
            elif len(i) == 6:
                pair[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]] += addend
            elif len(i) == 7:
                pair[i[0]][i[1]][i[2]][i[3]][i[4]][i[5]][i[6]] += addend
    # zero out pair
    pair[idx_list[0]][idx_list[1]][idx_list[2]][idx_list[3]] = 0
    return pair

def pairsplit(pair, check_right = True):
    for i in range(len(pair)):
        if type(pair[i]) != list and pair[i]>9:
            pair[i] = [int(np.floor(pair[i]/2)),int(np.ceil(pair[i]/2))]
            check_right = False
            break
        elif type(pair[i])==list and check_right:
            pair[i],check_right = pairsplit(pair[i])
            if not check_right:
                break
    return pair,check_right

def homework():
    sums = None
    for line in lines:
        line = json.loads(line)
        if sums:
            sums = snailadd(sums, line)
        else:
            sums = line
        #print(sums)
    print(snailmagnitude(sums))

def homework2():
    max_mag = 0
    for i in lines:
        for j in lines:
            if i != j:
                pair_sum = snailadd(json.loads(i),json.loads(j))
                pair_mag = snailmagnitude(pair_sum)
                max_mag = max([pair_mag,max_mag])
    print(max_mag)


def test_depth():
    for line in lines:
        print(depth(json.loads(line)))
#test_depth()

#print(snailreduced([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]))


homework()
homework2()
