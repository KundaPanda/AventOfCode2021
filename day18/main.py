import copy
import heapq
import json
from dataclasses import dataclass
from itertools import permutations
from math import ceil, floor
from typing import Optional, Union


@dataclass
class SnailFish:
    depth: int
    value: int
    left: Optional['SnailFish']
    right: Optional['SnailFish']
    alive: bool = True

    @property
    def leftmost(self):
        return self if self.left is None else self.left.leftmost

    @property
    def rightmost(self):
        return self if self.right is None else self.right.rightmost

    @property
    def leftmost_index(self):
        i = 0
        left = self.left
        while left:
            i += 1
            left = left.left
        return i

    def nest(self):
        self.depth += 1
        if self.right:
            self.right.nest()

    def __lt__(self, other):
        if not isinstance(other, SnailFish):
            return False
        if self.depth < other.depth:
            return True
        return self.value < other.value

    def __str__(self):
        val = f'{self.value}'
        return f'{val}, {self.right}' if self.right else f'{val}'


def load(lst, depth=0):
    a, b = lst
    if isinstance(a, list):
        a = load(a, depth + 1)
    else:
        a = SnailFish(depth, a, None, None)
    if isinstance(b, list):
        b = load(b, depth + 1)
        b.left = a.rightmost
    else:
        b = SnailFish(depth, b, a.rightmost, None)
    a.rightmost.right = b
    return a


def explode(fish: SnailFish):
    if fish.depth == 4:
        if fish.left:
            fish.left.value += fish.value
        if fish.right.right:
            fish.right.right.value += fish.right.value
            fish.right.right.left = fish
        fish.right.alive = False
        fish.right = fish.right.right
        fish.value = 0
        fish.depth -= 1
        return [fish.left, fish.right]
    return [None, None]


def split(fish: SnailFish):
    if fish.value >= 10:
        new = SnailFish(fish.depth + 1, ceil(fish.value / 2), fish, fish.right)
        if fish.right:
            fish.right.left = new
        fish.right = new
        fish.value = floor(fish.value / 2)
        fish.depth += 1
        return [fish, fish.right]
    return [None, None]


class HeapQ:
    def __init__(self):
        self.stack = []

    def push(self, value):
        heapq.heappush(self.stack, value)

    def pop(self):
        value = heapq.heappop(self.stack)
        return value

    def __len__(self):
        return len(self.stack)


@dataclass
class Pair:
    left: Union['Pair', SnailFish]
    right: Union['Pair', SnailFish]
    depth: int

    @property
    def value(self):
        return self.__str__()

    def __iter__(self):
        for item in json.loads(self.__str__()):
            yield item

    def __str__(self):
        return f'[{self.left.value}, {self.right.value}]'


def get_pairs(fish: SnailFish):
    fish_list = []
    node = fish
    while node:
        fish_list.append(node)
        node = node.right
    i = 0
    depth = 3
    while len(fish_list) != 1:
        any_changed = False
        while i < len(fish_list) - 1:
            if fish_list[i].depth == fish_list[i + 1].depth == depth:
                any_changed = True
                fish_list[i] = Pair(fish_list[i], fish_list[i + 1], fish_list[i].depth - 1)
                fish_list.pop(i + 1)
            i += 1
        i = 0
        if not any_changed:
            depth -= 1
    return fish_list[0]


def magnitude(value: Union[Pair, SnailFish]):
    if isinstance(value, SnailFish):
        return value.value
    return 3 * magnitude(value.left) + 2 * magnitude(value.right)


def add(left: SnailFish, right: SnailFish):
    right.left = left.rightmost
    left.rightmost.right = right
    left.nest()
    i = 0
    stack = HeapQ()
    fish = left
    while fish:
        stack.push((i, fish, explode))
        stack.push((1000 + i, fish, split))
        fish = fish.right
        i += 1
    while len(stack) != 0:
        priority, fish, operation = stack.pop()
        if not fish.alive:
            continue
        l, r = operation(fish)
        if operation == explode:
            if l:
                stack.push((1000 + priority - 1, l, split))
            if r:
                stack.push((1000 + priority + 1, r, split))
        else:
            if l:
                stack.push((priority - 1000, l, explode))
                stack.push((priority, l, split))
            if r:
                stack.push((priority + 1 - 1000, r, explode))
                stack.push((priority + 1, r, split))
    return left.leftmost


def part1():
    with open('input.txt', 'r') as f:
        data = [load(json.loads(line.strip())) for line in f.readlines()]
    first_fish = data[0]
    for i in range(1, len(data)):
        first_fish = add(first_fish, data[i])
    pairs = get_pairs(first_fish)
    print(magnitude(pairs))


def part2():
    with open('input.txt', 'r') as f:
        data = [load(json.loads(line.strip())) for line in f.readlines()]
    max_magnitude = 0
    for pair in permutations(data, 2):
        left = add(*[copy.deepcopy(fish) for fish in pair])
        if (magnitude_ := magnitude(get_pairs(left))) > max_magnitude:
            max_magnitude = magnitude_
    print(max_magnitude)


if __name__ == '__main__':
    part1()
    part2()
