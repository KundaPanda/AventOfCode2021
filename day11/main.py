from collections import deque

import numpy as np

brackets_map = {')': '(', ']': '[', '>': '<', '}': '{'}


def apply_light(arr, y, x, stack):
    if arr[y, x] == 0:
        return 0
    arr[y, x] = 0
    for yi in range(y - 1, y + 2):
        for xi in range(x - 1, x + 2):
            if 0 < arr[yi, xi] < 10:
                arr[yi, xi] += 1
            if arr[yi, xi] > 9:
                stack.append([yi, xi])
    return 1


def part1():
    arr = np.genfromtxt('input.txt', dtype=np.float32, delimiter=1)
    arr = np.pad(arr, [(1, 1), (1, 1)], mode='constant', constant_values=-np.inf)
    ones = np.ones_like(arr)
    lights = 0
    for _ in range(100):
        arr += ones
        stack = deque(np.argwhere(arr > 9))
        while len(stack) != 0:
            y, x = stack.pop()
            lights += apply_light(arr, y, x, stack)
    print(arr)
    print(lights)


def part2():
    arr = np.genfromtxt('input.txt', dtype=np.float32, delimiter=1)
    total = arr.shape[0] * arr.shape[1]
    arr = np.pad(arr, [(1, 1), (1, 1)], mode='constant', constant_values=-np.inf)
    ones = np.ones_like(arr)
    step = 0
    while 1:
        step += 1
        lights = 0
        arr += ones
        stack = deque(np.argwhere(arr > 9))
        while len(stack) != 0:
            y, x = stack.pop()
            lights += apply_light(arr, y, x, stack)
        if lights == total:
            print(step)
            return


if __name__ == '__main__':
    part1()
    part2()
