import math


def part1():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    increases = 0
    previous = math.inf
    for line in lines:
        if int(line) > previous:
            increases += 1
        previous = int(line)
    print(f"Total {increases} increases in depth")


def part2():
    with open('input.txt', 'r') as f:
        lines = [int(l) for l in f.readlines()]
    increases = 0
    previous = math.inf
    values = [sum(lines[i:i+3]) for i in range(len(lines) - 2)]
    for value in values:
        if value > previous:
            increases += 1
        previous = value
    print(f"Total {increases} increases in depth - sliding window")


if __name__ == '__main__':
    part1()
    part2()

