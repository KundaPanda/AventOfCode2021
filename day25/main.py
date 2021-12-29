import enum
from dataclasses import dataclass
from typing import List, Optional


class Direction(enum.Enum):
    RIGHT = '>'
    DOWN = 'v'

    @staticmethod
    def load(value: str):
        if value == '.':
            return None
        return Direction(value)


@dataclass
class Node:
    down: 'Node' = None
    right: 'Node' = None
    direction: Optional[Direction] = None

    def __eq__(self, other):
        return self is other

    def neighbor(self, direction: Direction):
        return self.down if direction == Direction.DOWN else self.right


def load_data():
    nodes = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            node = None
            for value in list(line.strip()):
                if not node:
                    node = Node(direction=Direction.load(value))
                    nodes.append(node)
                else:
                    node.right = Node(direction=Direction.load(value))
                    node = node.right
            node.right = nodes[-1]
    for row in range(len(nodes)):
        upper = nodes[row]
        lower = nodes[(row + 1) % len(nodes)]
        while 1:
            upper.down = lower
            upper, lower = upper.right, lower.right
            if upper == nodes[row]:
                break
    return nodes


def step(nodes: List[Node]):
    moved = 0
    for direction in [Direction.RIGHT, Direction.DOWN]:
        selected_nodes = []
        for row in nodes:
            node = row
            while 1:
                if node.direction == direction and not node.neighbor(direction).direction:
                    selected_nodes.append(node)
                node = node.right
                if node == row:
                    break
        for node in selected_nodes:
            neighbor = node.neighbor(direction)
            moved += 1
            node.direction, neighbor.direction = neighbor.direction, node.direction
    return moved


def print_nodes(nodes: List[Node]):
    data = []
    for row in nodes:
        node = row
        while 1:
            data.append(node.direction.value if node.direction else '.')
            node = node.right
            if node == row:
                break
        data.append('\n')
    print(''.join(data))


def part1():
    data = load_data()
    moved = -1
    rounds = 0
    while moved != 0:
        moved = step(data)
        rounds += 1
    print(rounds)


def part2():
    data = load_data()


if __name__ == '__main__':
    part1()
    part2()
