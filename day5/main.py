from collections import defaultdict


def part1():
    with open('input.txt', 'r') as f:
        lines = [line.split(" -> ") for line in f.readlines()]
    counts = defaultdict(int)
    for (start, end) in lines:
        x1, y1 = map(int, start.split(','))
        x2, y2 = map(int, end.split(','))
        if x1 == x2:
            for yi in range(min(y1, y2), max(y1, y2) + 1):
                counts[(x1, yi)] += 1
        elif y1 == y2:
            for xi in range(min(x1, x2), max(x1, x2) + 1):
                counts[(xi, y1)] += 1
    print(sum(v > 1 for v in counts.values()))


def part2():
    with open('input.txt', 'r') as f:
        lines = [line.split(" -> ") for line in f.readlines()]
    counts = defaultdict(int)
    for (start, end) in lines:
        x1, y1 = map(int, start.split(','))
        x2, y2 = map(int, end.split(','))
        if x1 == x2:
            for yi in range(min(y1, y2), max(y1, y2) + 1):
                counts[(x1, yi)] += 1
        elif y1 == y2:
            for xi in range(min(x1, x2), max(x1, x2) + 1):
                counts[(xi, y1)] += 1
        else:
            x0 = min(x1, x2)
            y0 = y1 if x0 == x1 else y2
            y_sign = 1 if y0 == min(y1, y2) else -1
            for i in range(max(x1, x2) - x0 + 1):
                counts[(x0 + i, y0 + (i * y_sign))] += 1
    print(sum(v > 1 for v in counts.values()))


if __name__ == '__main__':
    part1()
    part2()
