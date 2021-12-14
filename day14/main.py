from collections import Counter, defaultdict
from pprint import pprint


def step(sequence, mappings):
    result = []
    for a, b in zip(sequence, sequence[1:]):
        part = ''.join([a, b])
        result.append(a)
        if (value := mappings.get(part)) is not None:
            result.append(value)
    result.append(sequence[-1])
    return result


def load_sequence():
    with open('input.txt', 'r') as f:
        sequence = list(f.readline().strip())
        f.readline()
        mappings = f.readlines()
    mappings = {
        line.split(' -> ')[0]: line.strip().split(' -> ')[1] for line in mappings
    }
    return sequence, mappings


def part1():
    sequence, mappings = load_sequence()
    for _ in range(10):
        sequence = step(sequence, mappings)
    counter = Counter(sequence)
    print(counter.most_common()[0][1] - counter.most_common()[-1][1])


def part2():
    sequence, mappings = load_sequence()
    sequence_map = defaultdict(int)
    for a, b in zip(sequence, sequence[1:]):
        part = ''.join([a, b])
        sequence_map[part] += 1
    for _ in range(40):
        new_map = defaultdict(int)
        for pair in sequence_map.keys():
            if (value := mappings.get(pair)) is not None:
                new_map[pair[0] + value] += sequence_map[pair]
                new_map[value + pair[1]] += sequence_map[pair]
            else:
                new_map[pair] += sequence_map[pair]
        sequence_map = new_map
    new_map = defaultdict(int)
    for pair in list(sequence_map.keys()):
        new_map[pair[0]] += sequence_map[pair]
    new_map[sequence[-1]] += 1
    common = sorted(new_map.values())
    print(common[-1] - common[0])


if __name__ == '__main__':
    part1()
    part2()
