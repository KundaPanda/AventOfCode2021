import binascii
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import List

from bitarray import bitarray


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GT = 5
    LT = 6
    EQ = 7


@dataclass
class Packet:
    version: int
    type_id: int
    value: bytes = 0
    length: int = 6

    @property
    def version_sum(self):
        return self.version

    @property
    def type_(self):
        return PacketType(self.type_id)

    @staticmethod
    def from_hex(hex_str: str):
        data = bitarray()
        data.frombytes(binascii.unhexlify(hex_str))
        return Packet.from_bits(data)

    @staticmethod
    def from_bits(data: bitarray):
        packet = Packet(version=int(data[:3].to01(), 2), type_id=int(data[3:6].to01(), 2))
        packet.__class__ = ValuePacket if packet.type_ == PacketType.LITERAL else OperatorPacket
        packet.load_bits(data)
        return packet

    def load_bits(self, data: bitarray):
        return


class ValuePacket(Packet):
    value: bytes = 0

    def load_bits(self, data: bitarray):
        i = 6
        while 1:
            self.value <<= 4
            self.value |= int(data[i + 1:i + 5].to01(), 2)
            if data[i] == 0:
                break
            i += 5
        i += 5
        self.length = i


class OperatorPacket(Packet):
    len_type: bool
    subpackets: List[Packet]

    @property
    def version_sum(self):
        return self.version + sum(map(lambda p: p.version_sum, self.subpackets))

    @property
    def value(self) -> int:
        match self.type_:
            case PacketType.SUM:
                return sum(p.value for p in self.subpackets)
            case PacketType.PRODUCT:
                return reduce(lambda a, b: a * b, [int(p.value) for p in self.subpackets])
            case PacketType.MIN:
                return min(int(p.value) for p in self.subpackets)
            case PacketType.MAX:
                return max(int(p.value) for p in self.subpackets)
            case PacketType.GT:
                return int(self.subpackets[0].value > self.subpackets[1].value)
            case PacketType.LT:
                return int(self.subpackets[0].value < self.subpackets[1].value)
            case PacketType.EQ:
                return int(self.subpackets[0].value == self.subpackets[1].value)

    def load_bits(self, data: bitarray):
        i = 6
        self.len_type = bool(data[i])
        self.subpackets = []
        if self.len_type:
            number_subpackets = int(data[7:18].to01(), 2)
            i = 18
            for _ in range(number_subpackets):
                self.subpackets.append(Packet.from_bits(data[i:]))
                i += self.subpackets[-1].length
        else:
            self.length = int(data[7:22].to01(), 2)
            i = 22
            while i != self.length + 22:
                self.subpackets.append(Packet.from_bits(data[i:]))
                i += self.subpackets[-1].length
        self.length = i


def part1():
    with open('input.txt', 'r') as f:
        data = f.readline().strip()
    packet = Packet.from_hex(data)
    print(packet.version_sum)


def part2():
    with open('input.txt', 'r') as f:
        data = f.readline().strip()
    packet = Packet.from_hex(data)
    print(int(packet.value))


if __name__ == '__main__':
    # part1()
    part2()
