from dataclasses import dataclass
from functools import reduce
from operator import mul
import common

inp = common.read_file('2021/16/data.txt').strip()
def to_bin(hex_data):
    val = bin(int(hex_data, 16))[2:]
    padding_len =  (-len(val))%4
    padding = '0'*padding_len
    return padding+val
binary = to_bin(inp)

# part 1 and 2

@dataclass
class Packet:
    version: int
    packet_type: int
    def get_value(self):
        return 0

@dataclass
class NumberPacket(Packet):
    number: int
    def get_value(self):
        return self.number

@dataclass
class OperatorPacket(Packet):
    child_packets: list
    def get_value(self):
        vals = [p.get_value() for p in self.child_packets]
        if self.packet_type == 0:
            return sum(vals)
        if self.packet_type == 1:
            return reduce(mul, vals, 1)
        if self.packet_type == 2:
            return min(vals)
        if self.packet_type == 3:
            return max(vals)
        if self.packet_type == 5:
            return 1 if vals[0] > vals[1] else 0
        if self.packet_type == 6:
            return 1 if vals[0] < vals[1] else 0
        if self.packet_type == 7:
            return 1 if vals[0] == vals[1] else 0

def read_num_packet_content(data, start, version, packet_type):
    acc = ''
    marker = data[start]
    acc += data[start+1:start+5]
    start += 5
    while marker == '1':
        marker = data[start]
        acc += data[start+1:start+5]
        start += 5
    packet = NumberPacket(version, packet_type, int(acc, 2))
    return start, packet

def read_op_packet_content(data, start, version, packet_type):
    size_type = ord(data[start]) - ord('0')
    if size_type == 0:
        expect_bits = int(data[start+1:start+16], 2)
        expect_count = -1
        start += 16
    else:
        expect_bits = -1
        expect_count = int(data[start+1:start+12], 2)
        start += 12
    off = start
    child_packets = []
    while (off-start) != expect_bits and len(child_packets) != expect_count:
        off, child = read_packet(data, off)
        child_packets.append(child)
    packet = OperatorPacket(version, packet_type, child_packets)
    return off, packet

def read_packet(data, start):
    version = int(data[start:start+3], 2)
    packet_type = int(data[start+3:start+6], 2)
    if packet_type == 4:
        return read_num_packet_content(data, start+6, version, packet_type)
    return read_op_packet_content(data, start+6, version, packet_type)

def calc_versions(packet: Packet):
    acc = packet.version
    if isinstance(packet, OperatorPacket):
        for child in packet.child_packets:
            acc += calc_versions(child)
    return acc

_, packet = read_packet(binary, 0)
print(calc_versions(packet))
print(packet.get_value())
