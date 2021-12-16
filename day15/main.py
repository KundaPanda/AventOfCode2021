import sys
from heapq import heappop, heappush

import numpy
import numpy as np

numpy.set_printoptions(threshold=sys.maxsize)


def load_map():
    map_ = np.genfromtxt('input.txt', dtype=np.float32, delimiter=1)
    return map_


def get_neighbors(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def search_map(map_):
    seen = set()
    stack = [(0, 1, 1)]
    end = (map_.shape[0] - 2, map_.shape[1] - 2)
    while len(stack) != 0:
        cost, x, y = heappop(stack)
        if (x, y) in seen:
            continue
        if (x, y) == end:
            print(cost)
            return cost
        seen.add((x, y))
        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in seen:
                heappush(stack, (cost + map_[ny, nx], nx, ny))


def part1():
    map_ = np.pad(load_map(), ((1, 1), (1, 1)), 'constant', constant_values=np.inf)
    search_map(map_)


def enlarge_map(map_):
    def get_val(index, value):
        value = (index // map_.shape[0]) + value
        return value if value < 10 else (value % 10) + 1

    new_map = np.tile(map_, 5)
    new_map = np.apply_along_axis(lambda arr: [get_val(i, v) for i, v in enumerate(arr)], 1, new_map)
    ones = np.ones_like(new_map)
    map_tile = np.copy(new_map)
    for i in range(1, 5):
        new_map = np.append(new_map, map_tile + (i * ones), axis=0)
    new_map = np.apply_along_axis(lambda arr: np.vectorize(lambda v: v if v < 10 else (v % 10) + 1)(arr), 1, new_map)
    return new_map


def part2():
    map_ = np.pad(enlarge_map(load_map()), ((1, 1), (1, 1)), 'constant', constant_values=np.inf)
    search_map(map_)


if __name__ == '__main__':
    part1()
    part2()
