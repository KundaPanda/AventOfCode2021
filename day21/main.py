import abc
import copy
import re
from dataclasses import dataclass
from itertools import cycle
from pprint import pprint
from typing import Any, Generator, Tuple


@dataclass
class Player:
    id: int
    position: int
    score: int = 0


@dataclass
class Die(abc.ABC):
    rolls: int = 1

    @abc.abstractmethod
    def roll(self) -> Generator[int, Any, None]:
        raise NotImplemented


class DeterministicDie(Die):
    def roll(self):
        i = 1
        while 1:
            yield i
            self.rolls += 1
            i += 1
            if i == 101:
                i = 1


def load_data():
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        players = [
            Player(int(re.findall(r'Player (\d+)', line)[0]), int(re.findall(r'position: (\d+)', line)[0]))
            for line in lines
        ]
    return players


def run(players, die):
    players_it = cycle(players)
    roll = die.roll()
    while 1:
        player = next(players_it)
        score_total = player.position + sum([next(roll), next(roll), next(roll)]) % 10
        position = score_total % 11 + score_total // 11
        player.score += position
        player.position = position
        if player.score >= 1000:
            return player, next(players_it)


def part1():
    players = load_data()
    die = DeterministicDie()
    won, lost = run(players, die)
    print(lost.score * die.rolls)


def sim_cache(fn):
    cache = {}

    def wrapper(current: Player, other: Player, number: int, throw_no=0):
        key = (current.id, current.position, other.position, current.score, other.score, number, throw_no)
        if res := cache.get(key):
            return res
        res = fn(current, other, number, throw_no)
        cache[key] = res
        return res

    return wrapper


@sim_cache
def simulate_throw(current: Player, other: Player, number: int, throw_no) -> Tuple[int, int]:
    result = [0, 0]
    if throw_no != 3:
        for i in range(1, 4):
            result = [a + b for a, b in
                      zip(result, simulate_throw(copy.copy(current), copy.copy(other), number + i, throw_no + 1))]
        return tuple(result)
    number = current.position + number
    current.position = number % 11 + number // 11
    current.score += current.position
    if current.score >= 21:
        return 1, 0
    return simulate_throw(copy.copy(other), copy.copy(current), 0)[::-1]


def part2():
    players = load_data()
    scores = simulate_throw(copy.copy(players[0]), copy.copy(players[1]), 0)
    print(max(scores))


if __name__ == '__main__':
    part1()
    part2()
