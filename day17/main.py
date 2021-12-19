import re
from math import ceil, sqrt

from PIL import Image, ImageDraw


def show_trajectory(x_speed, y_speed, x0, y0, x1, y1):
    img = Image.new("RGB", (2000, 5000), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle(((x0 + 300, y0 + 300), (x1 + 300, y1 + 300)), 'blue')
    x, y = 0, 0
    xs, ys = x_speed, y_speed
    while not (y1 >= y >= y0 and x0 <= x <= x1):
        print(x, y)
        draw.point((x + 300, y + 300), 'green')
        x += xs
        y += ys
        if xs != 0:
            xs -= 1
        ys -= 1
    draw.point((x + 300, y + 300), 'green')
    draw.point((300, 300), 'red')
    img.rotate(180)
    img.show()


def get_speed_for(coord):
    return ceil((sqrt(8 * coord + 1) - 1) / 2)


def part1(show=False):
    with open('input.txt', 'r') as f:
        data = f.readline().strip()
    x0, x1, y0, y1 = map(int, re.findall(r"^target area: x=(\d+)..(\d+), y=(-\d+)..(-\d+)$", data)[0])
    x_speed = get_speed_for(x0)
    y_speed = 0 - y0 - 1
    y1 = (y_speed + 1) * y_speed / 2
    print(y1)
    if show:
        show_trajectory(x_speed, y_speed, x0, y0, x1, y1)


def part2():
    with open('input.txt', 'r') as f:
        data = f.readline().strip()
    x0, x1, y0, y1 = map(int, re.findall(r"^target area: x=(\d+)..(\d+), y=(-\d+)..(-\d+)$", data)[0])
    valid = 0
    for xs_ in range(get_speed_for(x0) - 1, x1 + 1):
        for ys_ in range(y0, -y0 + 1):
            x, y = 0, 0
            xs, ys = xs_, ys_
            while (x <= x1) and (y >= y0):
                if (x0 <= x <= x1) and (y0 <= y <= y1):
                    valid += 1
                    break
                x += xs
                y += ys
                if xs != 0:
                    xs -= 1
                ys -= 1
    print(valid)


if __name__ == '__main__':
    part1()
    part2()
