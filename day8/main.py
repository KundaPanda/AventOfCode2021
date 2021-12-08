from collections import Counter
from typing import List, Set


def part1():
    with open('input.txt', 'r') as f:
        inputs = [(part.split(' ') for part in line.strip().split(' | ')) for line in f.readlines()]
    counter = Counter()
    task2 = []
    for numbers, output in inputs:
        numbers: List[Set[int]] = sorted([set(n) for n in numbers], key=lambda n: len(n))
        num_dict = {
            1: numbers[0],
            7: numbers[1],
            4: numbers[2],
            8: numbers[-1],
        }
        remaining_nums = numbers[3:-1]
        num_dict[6], = [n for n in remaining_nums if len(n) == 6 and len(n & num_dict[1]) == 1]
        num_dict[9], = [n for n in remaining_nums if len(n) == 6 and len(n & num_dict[4]) == 4]
        remaining_nums.remove(num_dict[6])
        remaining_nums.remove(num_dict[9])
        num_dict[0], = [n for n in remaining_nums if len(n) == 6]
        remaining_nums.remove(num_dict[0])
        num_dict[2], = [n for n in remaining_nums if len(n & num_dict[9]) == 4]
        num_dict[3], = [n for n in remaining_nums if len(n & num_dict[1]) == 2]
        num_dict[5], = [n for n in remaining_nums if len(n & num_dict[6]) == 5]

        num_map = {frozenset(num_dict[k]): k for k in num_dict.keys()}
        output = [frozenset(n) for n in output]
        counter.update([num_map.get(key, None) for key in output])
        task2.append(int(''.join(str(num_map[key]) for key in output)))
    print(f'Task1: {sum([v for k, v in counter.items() if k in [1, 4, 7, 8]])}')
    print(f'Task2: {sum(task2)}')


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
