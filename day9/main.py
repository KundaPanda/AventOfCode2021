import sys
from collections import deque
from dataclasses import dataclass
from typing import Optional

import numpy as np

np.set_printoptions(threshold=sys.maxsize)


def is_low(arr, y, x):
    return all([arr[y, x - 1] > arr[y, x],
                arr[y - 1, x] > arr[y, x],
                arr[y + 1, x] > arr[y, x],
                arr[y, x + 1] > arr[y, x]])


def part1():
    map_: np.ndarray = np.genfromtxt('input.txt', dtype=np.float32, delimiter=1)
    map_ = np.pad(map_, [(1, 1), (1, 1)], mode='constant', constant_values=np.inf)
    result = np.zeros_like(map_)
    for y in range(1, map_.shape[0] - 1):
        for x in range(1, map_.shape[1] - 1):
            if is_low(map_, y, x):
                result[y, x] = map_[y, x] + 1
    print(np.sum(result))


@dataclass
class MapTile:
    value: int
    marked: bool = False
    basin: Optional[int] = None


def neighbors(y, x):
    return [(y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x)]


def part2():
    map_: np.ndarray = np.genfromtxt('input.txt', dtype=np.float32, delimiter=1)
    map_ = np.pad(map_, [(1, 1), (1, 1)], mode='constant', constant_values=np.inf)
    np.vectorize(MapTile)(map_)
    basins = []
    for y in range(1, map_.shape[0] - 1):
        for x in range(1, map_.shape[1] - 1):
            if is_low(map_, y, x):
                stack = deque(neighbors(y, x))
                basins.append({(y, x)})
                while not len(stack) == 0:
                    (ty, tx) = stack.pop()
                    if map_[ty, tx] >= 9 or (ty, tx) in basins[-1]:
                        continue
                    basins[-1].add((ty, tx))
                    stack.extendleft(neighbors(ty, tx))
    basins.sort(key=len, reverse=True)
    print(len(basins[0]) * len(basins[1]) * len(basins[2]))


if __name__ == '__main__':
    part1()
    part2()
