from collections import deque
from dataclasses import dataclass, field
from pprint import pprint
from typing import List


@dataclass
class GraphNode:
    name: str
    neighbors: List['GraphNode'] = field(default_factory=lambda: [])

    @property
    def small(self):
        return self.name.islower()


def load_nodes():
    with open('input.txt', 'r') as f:
        lines: List[str] = f.readlines()
    nodes = {
        'start': GraphNode('start'),
        'end': GraphNode('end'),
    }
    for line in lines:
        from_, to = line.strip().split('-')
        if from_ not in nodes:
            nodes[from_] = GraphNode(from_)
        if to not in nodes:
            nodes[to] = GraphNode(to)
        nodes[from_].neighbors.append(nodes[to])
        nodes[to].neighbors.append(nodes[from_])
    return nodes


def part1():
    nodes = load_nodes()
    stack = deque([(nodes['start'], ['start'])])
    paths = []
    while len(stack) != 0:
        node, path = stack.pop()
        if node.name == 'end':
            paths.append(path)
            continue
        for neighbor in node.neighbors:
            if (neighbor.small and neighbor.name not in path) or not neighbor.small:
                stack.appendleft((neighbor, path + [neighbor.name]))
    print(len(paths))


def part2():
    nodes = load_nodes()
    stack = deque([(nodes['start'], ['start'], False)])
    paths = 0
    while len(stack) != 0:
        node, path, small = stack.pop()
        for neighbor in node.neighbors:
            if neighbor.name == 'end':
                paths += 1
                continue
            if (neighbor.small and neighbor.name not in path) or not neighbor.small:
                stack.appendleft((neighbor, path + [neighbor.name], small))
            elif neighbor.small and neighbor.name in path and not small and neighbor.name != 'start':
                stack.appendleft((neighbor, path + [neighbor.name], True))
    print(paths)


if __name__ == '__main__':
    part1()
    part2()
