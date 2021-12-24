from load import openfile

# bailing on this build, starting from scratch to figure out how to proceed and make this work

today = "Day16"
lines = openfile(today+".txt")

binhex = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101",
          "6": "0110", "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011",
          "C": "1100", "D": "1101", "E": "1110", "F": "1111"}


def parse_to_bin(hex_string):
    bin_string = ""
    for i in hex_string:
        bin_string += binhex[i]
    return bin_string


bits = parse_to_bin(lines)

pos = 0
package = {}
package_key = None
for bit in bits:
    # check to see if end of package reached
    if bits[pos:] == "0"*len(bits[pos:0]):
        break












def parse_bits(bin_string, position):
    packets = []
    while position < len(bin_string):
        next_packet = Packet(bin_string[position:position+6])
        if next_packet.type == "literal":
            eos = position + 10
            while bin_string[eos-4] != 0:
                eos += 5
            next_packet.assign_value_from_bin(bin_string[position+6:eos])
            position = eos + 1
        elif next_packet.type == "operator":
            next_packet.read_length_type(bin_string[position+6], bin_string[position+7:position+22])




        packets.append(next_packet)

    return packets


class Packet:
    def __init__(self, header):
        self.header = header
        self.input_string = header
        self.version_num = self.header[0:3]
        self.type_id = self.header[3:6]
        self.type = "literal" if self.type_id == "100" else "operator"
        self.value = None
        self.sub_packet_count = None
        self.packet_count_bin_len = None
        self.sub_count_type = None

    def assign_value_from_bin(self, bin_string):
        reduced_bin = ""
        for segnum in range(len(bin_string)/5):
            reduced_bin = bin_string[1+segnum*5:5+segnum*5]
        self.value = reduced_bin

    def read_length_type(self, bit, next15):
        if bit==0: # read as total len in bits
            self.sub_count_type = "length"
            self.packet_count_bin_len = 15
            self.sub_packet_count = int(next15, 2)
        elif bit==1: # read as total num of packets
            self.sub_count_type = "count"
            self.packet_count_bin_len = 11
            self.sub_packet_count = int(next15[0:11], 2)






def problem1():
    bin_string = parse_to_bin(lines)
    packets = parse_bits(bin_string, 0)

