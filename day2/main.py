from enum import Enum


class Action(Enum):
    UP = 'up'
    DOWN = 'down'
    FORWARD = 'forward'

    def apply1(self, value, plane):
        if self == self.UP:
            plane.vertical -= value
        elif self == self.DOWN:
            plane.vertical += value
        else:
            plane.horizontal += value

    def apply2(self, value, plane):
        if self == self.UP:
            plane.aim -= value
        elif self == self.DOWN:
            plane.aim += value
        else:
            plane.horizontal += value
            plane.vertical += plane.aim * value


class Plane:
    def __init__(self):
        self.vertical = 0
        self.horizontal = 0
        self.aim = 0

    def apply1(self, lines):
        for line in lines:
            Action(line[0]).apply1(int(line[1]), self)

    def apply2(self, lines):
        for line in lines:
            Action(line[0]).apply2(int(line[1]), self)


def part1():
    with open('input.txt', 'r') as f:
        lines = [line.split(" ") for line in f.readlines()]
    plane = Plane()
    plane.apply1(lines)
    print(plane.horizontal * plane.vertical)


def part2():
    with open('input.txt', 'r') as f:
        lines = [line.split(" ") for line in f.readlines()]
    plane = Plane()
    plane.apply2(lines)
    print(plane.horizontal * plane.vertical)


if __name__ == '__main__':
    part1()
    part2()
