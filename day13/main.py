from typing import Set, Tuple

import numpy as np
from PIL import Image, ImageColor


def fold(dots: Set[Tuple[int, ...]], axis, value):
    new_dots = set()
    for (x, y) in dots:
        if axis == 'x' and x > value:
            new_dots.add((x - (x - value) * 2, y))
        elif axis == 'y' and y > value:
            new_dots.add((x, y - (y - value) * 2))
        else:
            new_dots.add((x, y))
    return new_dots


def load_dots():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    fold_ = False
    dots: Set[Tuple[int, ...]] = set()
    folds = []
    for line in lines:
        if line == '\n':
            fold_ = True
            continue
        if fold_:
            axis, value = line.split()[-1].split('=')
            folds.append((axis, int(value)))
        else:
            dots.add(tuple(map(int, line.split(','))))
    return dots, folds


def part1():
    dots, folds = load_dots()
    dots = fold(dots, *folds[0])
    print(len(dots))


def part2():
    dots, folds = load_dots()
    for fold_ in folds:
        dots = fold(dots, *fold_)
    a = np.array(list(dots), dtype=np.dtype('int,int'))
    image = Image.new('RGB', (np.max(a['f0'] + 1), np.max(a['f1'] + 1)))
    for dot in dots:
        image.putpixel(dot, ImageColor.getcolor('white', 'RGB'))
    image.show()


if __name__ == '__main__':
    part1()
    part2()
