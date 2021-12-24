from load import openfile

# bailing on this build, starting from scratch to figure out how to proceed and make this work

today = "Day16"
lines = openfile(today + ".txt")
input_bits = lines[0]

binhex = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101",
          "6": "0110", "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011",
          "C": "1100", "D": "1101", "E": "1110", "F": "1111"}


class Packet: # packet class to hold packet basic information
    def __init__(self, header):
        self.header = header
        self.version_num = int(header[0:3], 2)
        self.type_id = int(header[3:6], 2)
        self.sub_packets = None
        self.value = None

    def get_version_sum(self):
        if self.value:
            return self.version_num
        else:
            sub_sum = sum(list(map(lambda i: i.get_version_sum(), self.sub_packets)))
            return sub_sum


def parse_to_bin(hex_string):
    bin_string = ""
    for i in hex_string:
        bin_string += binhex[i]
    return bin_string


def get_value(bits):
    bin_total = ""
    for segnum in range(len(bits) // 5):
        bin_total += bits[1 + segnum * 5:5 + segnum * 5]
    return int(bin_total, 2)


def read_bits(bits, packets_remaining=1, sub_packet_bit_length=None):
    packets = []
    pos = 0  # pos of beginning of bin string
    # loop until number of expected packets is 0
    while packets_remaining > 0:
        #initalize a packet with its header
        new_packet = Packet(bits[0 + pos:6 + pos])
        # if type is 4, its a literal value
        if new_packet.type_id == 4:
            eos = 11 + pos #end of this string should be read in bunches of 5 from this spot until there is a 1 at the start of those bunches
            while bits[eos - 4] == "1":
                eos += 5
            new_packet.value = get_value(bits[6 + pos:eos])
            pos = eos
        else:
            length_type_id = bits[pos + 6]
            if length_type_id == '0':
                length_in_bits = int(bits[pos + 7:pos + 22], 2)
                eos = pos + 22 + length_in_bits
                new_packet.sub_packets = read_bits(bits[pos + 22:eos + 1], 1, length_in_bits)
            else:
                packet_count = int(bits[pos + 7:pos + 18], 2)
                new_packet.sub_packets = read_bits(bits[pos + 18:], packet_count)
        packets.append(new_packet)
        packets_remaining -= 1
        if sub_packet_bit_length and pos != sub_packet_bit_length:
            packets_remaining += 1
    return packets


input_bits = parse_to_bin(input_bits)
#read_bits(input_bits)
short_reading = read_bits(parse_to_bin("8A004A801A8002F478"))
for packet in short_reading:
    print(packet.get_version_sum())
medium_reading = read_bits(parse_to_bin("620080001611562C8802118E34"))
for packet in medium_reading:
    print(packet.get_version_sum())
