from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Fish:
    cycle: int

    def run_once(self, fish: list):
        if self.cycle == 0:
            self.cycle = 7
            fish.append(Fish(9))
        self.cycle -= 1


def sim(fish: List[Fish], rounds=80):
    for _ in range(rounds):
        for f in fish:
            f.run_once(fish)


def sim2(fish: Dict[int, int], rounds=256):
    for _ in range(rounds):
        fish_0 = fish[0]
        for i in range(8):
            fish[i], fish[i+1] = fish[i+1], fish[i]
        fish[6] += fish_0


def part1():
    with open('input.txt', 'r') as f:
        fish = list(map(lambda n: Fish(int(n)), f.readline().split(',')))
    sim(fish)
    print(len(fish))


def part2():
    fish = {n: 0 for n in range(9)}
    with open('input.txt', 'r') as f:
        fish.update(Counter(map(int, f.readline().split(','))))
    sim2(fish)
    print(sum(fish.values()))


if __name__ == '__main__':
    part1()
    part2()
