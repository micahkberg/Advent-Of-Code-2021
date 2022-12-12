from load import openfile

today = "Day24"
lines = openfile(today+".txt")
lines = lines[:-1]
# print(lines)

class ALU:
    def __init__(self):
        self.status = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.digits = ""

    def __repr__(self):
        rep = f"[<ALU object #{self.digits}, {self.status}>]"
        return rep

    def check_value(self, b):
        if b not in "wxyz":
            return int(b)
        else:
            return self.status[b]

    def inp_a(self, a, value):
        self.status[a] = value
        self.digits = self.digits + str(value)

    def add_a_b(self, a, b):
        self.status[a] += self.check_value(b)

    def mul_a_b(self, a, b):
        self.status[a] *= self.check_value(b)

    def div_a_b(self, a, b):
        self.status[a] //= self.check_value(b)

    def mod_a_b(self, a, b):
        self.status[a] = self.status[a]%self.check_value(b)

    def eql_a_b(self, a, b):
        self.status[a] = 1 if self.status[a] == self.check_value(b) else 0

    def read_line(self, line, value):
        parts = line.split(" ")
        line_func_dict = {"inp": self.inp_a,
                          "add": self.add_a_b,
                          "mul": self.mul_a_b,
                          "div": self.div_a_b,
                          "mod": self.mod_a_b,
                          "eql": self.eql_a_b,}
        func = line_func_dict[parts[0]]
        if func == self.inp_a:
            func(parts[1], value)

        else:
            func(parts[1], parts[2])


#def part1_brute_force():
#    testing_num = int("9"*14)
#    while True:
#        new_alu = ALU()
#        current_digit = 13
#        for line in lines:
#            if new_alu.read_line(line, int(str(testing_num)[current_digit])):
#                current_digit -= 1
#        if new_alu.status["z"]==0:
#            print(testing_num)
#            break
#        else:
#            print(testing_num)
#            testing_num -= 1
#            while "0" in str(testing_num):
#                testing_num -= 1


#def part1_one_input_at_a_time():
#    list_of_possible_states = [ALU()]
#    for line in lines:
#        new_states = []
#        set_states = set()
#        for machine_state in list_of_possible_states:
#            resulting_states = machine_state.read_line(line)
#            for new_state in resulting_states:
#                if tuple(new_state.status.values()) not in set_states:
#                    set_states.add(tuple(new_state.status.values()))
#                    new_states.append(new_state)
#                else:
#                    for state in new_states:
#                        if state.status == new_state.status:
#                            state.digits = new_state.digits if int(new_state.digits) > int(state.digits) else state.digits
#                            break
#        list_of_possible_states = new_states.copy()
#        print(f"{line}: {len(list_of_possible_states)}")
#
#
#    big_one = 0
#    for state in list_of_possible_states:
#        if state.status["z"] == 0 and int(state.digits) > big_one:
#            big_one = int(state.digits)
#    print(big_one)


#def part1_whole_leg_calcs():
#
#    # splitting all the lines into segments that start with inp w
#    command_segments = []
#    new_segment = []
#    times_input = 0
#    for line in lines:
#        if line.split(" ")[0] == "inp":
#            times_input+=1
#
#        if times_input<2:
#            new_segment.append(line)
#        else:
#            command_segments.append(new_segment.copy())
#            times_input = 1
#            new_segment = [line]
#    command_segments.append(new_segment.copy())
#
#    # list we will iterate across to make new states
#    list_of_possible_states = [ALU()]
#    for command_segment in command_segments:
#        new_states = []
#        set_statuses = set()
#        for machine_state in list_of_possible_states:
#            for digit in range(1,10):
#                new_machine = ALU()
#                new_machine.digits = machine_state.digits
#                new_machine.status = machine_state.status.copy()
#                for line in command_segment:
#                    new_machine.read_line(line, digit)
#                machine_status_tuple = tuple(new_machine.status.values())
#                if machine_status_tuple not in set_statuses:
#                    set_statuses.add(machine_status_tuple)
#                    new_states.append(new_machine)
#                else:
#                    match_found = False
#                    for state in new_states:
#                        if state.status == new_machine.status:
#                            state.digits = new_machine.digits if int(new_machine.digits) > int(state.digits) else state.digits
#                            match_found = True
#                            break
#                    if not match_found:
#                        print("Error: found match in set, but didnt find match in list")
#            list_of_possible_states = new_states.copy()
#        print(f"{len(list_of_possible_states[0].digits)}: {len(list_of_possible_states)}")
#
#    big_one = 0
#    for state in list_of_possible_states:
#        if state.status["z"] == 0 and int(state.digits) > big_one:
#            big_one = int(state.digits)
#    print(big_one)




#    # splitting all the lines into segments that start with inp w
command_segments = []
new_segment = []
times_input = 0
for line in lines:
    if line.split(" ")[0] == "inp":
        times_input+=1

    if times_input<2:
        new_segment.append(line)
    else:
        command_segments.append(new_segment.copy())
        times_input = 1
        new_segment = [line]
command_segments.append(new_segment.copy())

a = list(map(lambda i:int(i[5].split(" ")[2]), command_segments))
b = list(map(lambda i: int(i[15].split(" ")[2]), command_segments))
divs = list(map(lambda i: int(i[4].split(" ")[2]), command_segments))
for i in range(len(command_segments[0])):
    line = f"{i+1} "
    for segment in command_segments:
        line += str.ljust(segment[i], 10)
    print(line)

print(f"a: {a}")
print(f"b: {b}")
print(divs)
z_nexts = {i: {} for i in range(14)}
z_nexts[13] = {0: set()}
#print(z_nexts)
digits = dict()


for n in range(13,-1,-1):
    for z_next_n in z_nexts[n].keys():
        possible_digit_n_values = set()
        b_n = b[n]
        a_n = a[n]
        divisor = divs[n]
        for d in range(1,10):
            # case 1
            # z0/divisor = z_next
            # and d_n = z0%26+a
            z0 = divisor * z_next_n
            if d == z0%26 + a_n and type(z0) == int:
                possible_digit_n_values.add(d)
                if z0 not in z_nexts[n].keys():
                    z_nexts[n-1][z0] = {d}
                else:
                    pass
            # case 2
            z0 = (z_next_n - d - b_n) * divisor / 26
            if d != z0%26 + a_n and type(z0) == int:
                possible_digit_n_values.add(d)
                print(z0)
        digits[n] = possible_digit_n_values

# finding 1 & 26 pairs
ones = []
pairs = []
big_digits = "00000000000000"
for i in range(len(divs)):
    if divs[i]==1:
        ones.append(i)
    else:
        pairs.append((ones.pop(-1),i))
for pair in pairs:
    print(f"d_{pair[0]}, d_{pair[1]}, {a[pair[1]]} + {b[pair[0]]} = {a[pair[1]] + b[pair[0]]}")

# just worked it out from hand from here since i spent so long on everything else lmao

#big 69914999975369
#little 14911675311114
