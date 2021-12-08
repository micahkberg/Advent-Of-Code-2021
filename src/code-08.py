from load import openfile

today = "Day08"
lines = openfile(today+".txt")
clocks = list(map(lambda i: list(map(lambda j: j.strip().split(" "), i.split("|"))), lines))[:-1]

count_ans_1 = 0

#letters solved for: a, d, c ,e ,f
length_ciphers = {
    0: 6, # done
    1: 2, # done
    2: 5,
    3: 5,
    4: 4, # done
    5: 5, # done
    6: 6, # done
    7: 3, # done
    8: 7, # done
    9: 6 # done
}

for clock in clocks:
    lens = list(map(lambda j: len(j), clock[1]))
    for leng in lens:
        if leng in [2,3,4,7]:
           count_ans_1 += 1
print("Part 1")
print(count_ans_1)


sum = 0
for clock in clocks:
    key = list(range(10))
    for number in clock[0]: # identify the numbers 1,4,7,8
        number = "".join(sorted(number))
        if len(number) == 2:
            key[1] = number
        elif len(number) == 3:
            key[7] = number
        elif len(number) == 4:
            key[4] = number
        elif len(number) == 7:
            key[8] = number

    for number in clock[0]: # identify the number 6
        if len(number) == 6 and not type(key[6]) == str:
            for letter in key[8]:
                if not letter in number and letter in key[1]:
                    c = letter
                    key[6] = "".join(sorted(number))
                    break

    for letter in key[1]: # now that we have c, get f
        if not letter in c:
            f = letter

    for letter in key[7]: # with c, f, get a
        if not letter in key[1]:
            a = letter

    for number in clock[0]: # with this info we can find 5
        if len(number) == 5 and not type(key[5])==str:
            is_five = False
            for letter in key[8]:
                if not letter in number:
                    if letter == c:
                        is_five = True
                    else:
                        maybe_e = letter
            if is_five:
                e = maybe_e # identify e while we are here
                key[5] = "".join(sorted(number))

    for number in clock[0]: # find 9
        if len(number) == 6 and not type(key[9])==str:
            for letter in key[8]:
                if not letter in number and letter == e:
                    key[9] = "".join(sorted(number))

    for number in clock[0]: # find 0
        if len(number) == 6 and not type(key[0])==str:
            for letter in key[8]:
                if letter not in number and letter not in [c,e]:
                    d = letter
                    key[0] = "".join(sorted(number))

    for number in clock[0]: # 2 or 3
        if len(number) == 5:
            missing = []
            for letter in key[8]:
                if letter not in number:
                    missing.append(letter)
            if c in missing and e in missing:
                pass
            elif e in missing:
                key[3] = "".join(sorted(number))
            elif f in missing:
                key[2] = "".join(sorted(number))

    # time to read the current number
    digits = []
    for digit in clock[1]:
        sorted_digit = "".join(sorted(digit))
        digits.append(key.index(sorted_digit))

    sum += 1000*digits[0] + 100*digits[1] + 10*digits[2] + digits[3]

print(sum)
