import re
from functools import reduce
from itertools import product
from typing import Tuple

import plotly.graph_objects as go


def load_data():
    with open('input.txt') as f:
        lines = [re.findall(r'(on|off) x=([-\d]+)..([-\d]+),y=([-\d]+)..([-\d]+),z=([-\d]+)..([-\d]+)', line.strip())[0]
                 for line in f.readlines()]
    lines = [(l[0], *tuple(int(coord) for coord in l[1:])) for l in lines]
    lines = [(l[0] == 'on', *list(zip(l[1::2], l[2::2]))) for l in lines]
    return lines


def volume(coords: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> int:
    return reduce(lambda a, b: a * b, [coord[1] - coord[0] + 1 for coord in coords])


def viz(coords):
    data = []
    for coord in coords:
        coord = list(product(*zip([c[0] - .5 for c in coord], [c[1] + .5 for c in coord])))
        data.append(go.Mesh3d(
            x=[c[0] for c in coord],
            y=[c[1] for c in coord],
            z=[c[2] for c in coord],
            showscale=True,
            alphahull=0
        ))
    fig = go.Figure(data=data)
    fig.show()


def get_bounded(coords, axis, value, x_bounds=(), y_bounds=()):
    x = (x_bounds[0][1] + 1 if x_bounds[0] else coords[0][0], x_bounds[1][0] - 1 if x_bounds[1] else coords[0][1])
    if axis == 1:
        return x, value, coords[2]
    y = (y_bounds[0][1] + 1 if y_bounds[0] else coords[1][0], y_bounds[1][0] - 1 if y_bounds[1] else coords[1][1])
    return x, y, value


def run_reboot(data, show=False):
    reactor = set()
    for state, x, y, z in data:
        for coords in list(reactor):
            new_bounds = []
            for ((c0, c1), (cb0, cb1)) in zip([x, y, z], coords):
                if cb0 < c0 < cb1:
                    if cb0 <= c1 < cb1:
                        new_bounds.append([(cb0, c0 - 1), (c1 + 1, cb1)])
                    else:
                        new_bounds.append([(cb0, c0 - 1), ()])
                elif cb0 == c0:
                    new_bounds.append([(), (c1 + 1, cb1)] if cb1 > c1 else [(), ()])
                elif cb1 == c0:
                    new_bounds.append([(cb0, cb1 - 1), ()])
                elif cb0 <= c1 < cb1:
                    new_bounds.append([(), (c1 + 1, cb1)])
                elif c1 == cb1:
                    new_bounds.append([(), ()])
                elif c0 <= cb0 <= cb1 <= c1:
                    new_bounds.append([(), ()])
            if len(new_bounds) == 3:
                for axis in range(3):
                    end, start = new_bounds[axis]
                    match axis:
                        case 0:
                            if end:
                                reactor.add((end, coords[1], coords[2]))
                            if start:
                                reactor.add((start, coords[1], coords[2]))
                        case 1:
                            if end:
                                reactor.add(get_bounded(coords, axis, end, new_bounds[0]))
                            if start:
                                reactor.add(get_bounded(coords, axis, start, new_bounds[0]))
                        case 2:
                            if end:
                                reactor.add(get_bounded(coords, axis, end, new_bounds[0], new_bounds[1]))
                            if start:
                                reactor.add(get_bounded(coords, axis, start, new_bounds[0], new_bounds[1]))
                reactor.remove(coords)
        if state:
            reactor.add((x, y, z))
        if show:
            viz(reactor)
    return reactor


def filter_50_50_cube(data):
    return ((-50, -50), (-50, -50), (-50, -50)) <= (data[1], data[2], data[3]) <= ((50, 50), (50, 50), (50, 50))


def part1():
    data = load_data()
    data = filter(filter_50_50_cube, data)
    reactor = run_reboot(data)
    print(sum(volume(k) for k in reactor))


def part2():
    data = load_data()
    reactor = run_reboot(data)
    print(sum(volume(k) for k in reactor))


if __name__ == '__main__':
    part1()
    part2()
