import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


BITS_VALUE = np.flip(np.logspace(0, 8, 9, base=2))


def load_array(string: str):
    return np.fromiter(string.replace('.', '0').replace('#', '1'), dtype=np.int32)


def load_data():
    with open('input.txt') as f:
        code = load_array(f.readline().strip())
        f.readline()
        image = np.array([load_array(line.strip()) for line in f.readlines()])
    image = np.pad(image, ((2, 2), (2, 2)), constant_values=0)
    return code, image


def apply_step(code, image):
    arr_type = np.zeros if code[image[0, 0]] == 0 else np.ones
    new_image = arr_type((image.shape[0] + 2, image.shape[1] + 2), dtype=np.int32)
    for y, row in enumerate(sliding_window_view(image, (3, 3))):
        for x, window in enumerate(row):
            new_image[y + 2, x + 2] = code[np.sum(window.flatten() * BITS_VALUE, dtype=np.int32)]
    return new_image


def apply_steps(code, image, steps=2):
    for _ in range(steps):
        image = apply_step(code, image)
    return image


def part1():
    code, image = load_data()
    image = apply_steps(code, image, 2)
    print(dict(zip(*np.unique(image, return_counts=True)))[1])


def part2():
    code, image = load_data()
    image = apply_steps(code, image, 50)
    print(dict(zip(*np.unique(image, return_counts=True)))[1])


if __name__ == '__main__':
    part1()
    part2()
