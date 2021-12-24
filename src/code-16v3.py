from load import openfile

today = "Day16"
lines = openfile(today+".txt")
hex_data = lines[0]

# how to translate bits
binhex = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101",
          "6": "0110", "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011",
          "C": "1100", "D": "1101", "E": "1110", "F": "1111"}


# translate bits
def parse_to_bin(hex_string):
    bin_string = ""
    for i in hex_string:
        bin_string += binhex[i]
    return bin_string

def prod(lis):
    out = 1
    for i in lis:
        out *= i
    return out

bin_data = parse_to_bin(hex_data)


class Packet:
    def __init__(self, contents):
        self.contents = contents
        self.header = contents[:6]
        self.version = self.header[:3]
        self.type_id = self.header[3:6]
        type_dict = {"000": "Sum",
                     "001": "Prod",
                     "010": "Min",
                     "011": "Max",
                     "100": "Lit",
                     "101": ">",
                     "110": "<",
                     "111": "="}
        self.type = type_dict[self.type_id]
        self.value = None
        self.length = None
        self.sub_packet_len = None
        self.sub_packet_count = None
        self.sub_packets = None
        if self.type == "Lit":
            self.value, self.length = self.get_lit_value()
        else:
            self.length_type_id = self.contents[6]
            if self.length_type_id == "0":
                self.set_sub_packet_len()
            elif self.length_type_id == "1":
                self.set_sub_packet_count()
            self.sub_packets = self.parse_sub_packets()
        if self.type != "Lit":
            self.sub_values = list(map(lambda i: i.value, self.sub_packets))
            print(list(self.sub_values))
            if self.type == "Sum":
                self.value = sum(self.sub_values)
            elif self.type == "Prod":
                self.value = prod(self.sub_values)
            elif self.type == "Max":
                self.value = max(self.sub_values)
            elif self.type == "Min":
                self.value = min(self.sub_values)
            elif self.type == ">":
                self.value = 1 if list(self.sub_values)[0] > list(self.sub_values)[1] else 0
            elif self.type == "<":
                self.value = 1 if list(self.sub_values)[0] < list(self.sub_values)[1] else 0
            elif self.type == "=":
                self.value = 1 if list(self.sub_values)[0] == list(self.sub_values)[1] else 0


    def set_sub_packet_len(self):
        len_bin = self.contents[7:22]
        self.sub_packet_len = int(len_bin, 2)
        self.length = 7+15+self.sub_packet_len

    def version_sum(self):
        if self.sub_packets:
            return sum(map(lambda i: i.version_sum(),self.sub_packets)) + int(self.version, 2)
        else:
            return int(self.version, 2)

    def set_sub_packet_count(self):
        count_bin = self.contents[7:18]
        self.sub_packet_count = int(count_bin,2)
        self.length = 7+11

    def get_lit_value(self):
        val_len = 0
        at0 = False
        while not at0:
            if self.contents[6+(val_len*5)] == "0":
                at0 = True
            val_len += 1
        binvalue = ""
        for i in range(val_len):
            binvalue += self.contents[7+5*i:11+5*i]
        value = int(binvalue, 2)
        length = 6+5*val_len
        #if length%4 != 0:               not sure that this is needed at all
        #    length += 4-(length % 4)+6
        return value, length

    def parse_sub_packets(self):
        packets = []
        total_len = 0
        if self.sub_packet_len:
            while total_len < self.sub_packet_len:
                new_packet = Packet(self.contents[22+total_len:])
                packets.append(new_packet)
                total_len+=new_packet.length
        elif self.sub_packet_count:
            while len(packets)<self.sub_packet_count:
                new_packet = Packet(self.contents[18+total_len:])
                packets.append(new_packet)
                total_len += new_packet.length
            self.length += total_len
        return packets


part1packet = Packet(bin_data)
#part1packet = Packet(parse_to_bin("9C0141080250320F1802104A08"))
print(f"data packet version check sum: {part1packet.version_sum()}")
print(f"packet value: {part1packet.value}")


