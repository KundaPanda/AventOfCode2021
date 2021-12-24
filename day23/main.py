import heapq
import math
from dataclasses import dataclass, field
from functools import cached_property
from textwrap import dedent
from typing import Any, Dict, Generator, List, Optional, Tuple

"""
########################
#0 1 2 3 4 5 6 7 8 9 10#
#####12##14##16##18#####
    #22##24##26##28#
    ################
"""


@dataclass
class Map:
    map_: Dict[int, Optional[int]] = field(default_factory=lambda: {i: 0 for i in range(11)})
    last_moved: int = None

    @cached_property
    def max_slot(self):
        return max(self.map_.keys()) - 6

    def slot_empty(self, slot: int):
        return all(self.map_[slot + i] in {0, slot} for i in range(10, self.max_slot, 10))

    def slot_top(self, slot: int):
        return next((i for i in range(slot + 10, self.max_slot + 7, 10) if self[i]), None)

    @property
    def filled_slots(self):
        res = 0
        for slot in range(2, 9, 2):
            for i in range(self.max_slot - 2, 9, -10):
                if self[slot + i] != slot:
                    break
                res += cost(slot)
        return res

    def _get_str(self, field_: int):
        value = self.map_.get(field_) or '.'
        return num_to_char(value) if isinstance(value, int) else value

    def copy(self):
        new_dict = self.map_.copy()
        other = Map(new_dict)
        return other

    def move(self, from_: int, to: int):
        m = self.copy()
        m[to], m[from_] = m[from_], 0
        m.last_moved = to
        return cost(m[to]) * abs(to - from_) // (1 if to < 11 and from_ < 11 else 10), m

    def move_empty(self, from_, *positions):
        for position in positions:
            if not self[position]:
                yield self.move(from_, position)

    @property
    def _distance_multiplier(self):
        m = 1
        for i in range(11):
            if self[i]:
                m *= (abs(self[i] - i) + 1)
        return m

    @property
    def won(self):
        return all(not self[i] for i in range(11)) and all(self.slot_empty(i) for i in range(2, 9, 2))

    @cached_property
    def as_str(self):
        return ','.join(map(str, self.map_.values()))

    def __getitem__(self, item):
        return self.map_[item]

    def __setitem__(self, key, value):
        self.map_[key] = value
        try:
            del self.as_str
        except AttributeError:
            pass

    def __str__(self):
        s = dedent(f'''\
        #############
        #{"".join(self._get_str(i) for i in range(11))}#
        ###{self._get_str(12)}#{self._get_str(14)}#{self._get_str(16)}#{self._get_str(18)}###
        ''')
        for i in range(22, max(self.map_.keys()) - 5, 10):
            s += f'  #{"#".join(self._get_str(i_) for i_ in range(i, i + 7, 2))}#\n'
        s += '  #########'
        return s

    def __lt__(self, other):
        if not isinstance(other, Map):
            return False
        return self.as_str < other.as_str


def cost(num):
    return pow(10, num // 2 - 1)


def char_to_num(c):
    match c:
        case 'A':
            return 2
        case 'B':
            return 4
        case 'C':
            return 6
        case 'D':
            return 8


def num_to_char(c):
    match c:
        case 2:
            return 'A'
        case 4:
            return 'B'
        case 6:
            return 'C'
        case 8:
            return 'D'


def load_data(part=1):
    map_ = Map()
    with open('input.txt' if part == 1 else 'input2.txt') as f:
        for i, line in enumerate(f.readlines()[2:]):
            if line.startswith('  ####'):
                break
            map_.map_.update(
                [((i + 1) * 10 + (i_ + 1) * 2, char_to_num(c)) for i_, c in enumerate(line[3:10].split('#'))])

    return map_


def get_all_moves(map_: Map) -> Generator[Tuple[int, Map], Any, None]:
    for i in range(2, 9, 2):
        # In front of empty slots
        if value := map_[i]:
            if i == value and map_.slot_empty(value):
                if top := map_.slot_top(i):
                    yield map_.move(i, top - 10)
                else:
                    yield map_.move(i, map_.max_slot - 2 + i)
                return
            yield from map_.move_empty(i, i + 1, i - 1)
            return
    # for stack in range(2, 9, 2):
    #     # Inside the stack
    #     for i in range(stack + 10, map_.max_slot - 10 + 7, 10):
    #         if map_[i] and not map_[i + 10] and map_[i] == stack and map_.slot_empty(stack):
    #             # Space within the stack, move there with priority
    #             yield map_.move(i, i + 10)
    #             return
    for i in range(11):
        # In the hallway, check for empty path
        if map_[i]:
            if map_.last_moved == i:
                steps = []
                if i < 10:
                    steps.append(i + 1)
                if i > 0:
                    steps.append(i - 1)
                yield from map_.move_empty(i, *steps)
            move_direction = range(i + 1, map_[i] + 1) \
                if i < map_[i] \
                else range(i - 1, map_[i] - 1, -1)
            if map_.slot_empty(map_[i]) and all(not map_[i_] for i_ in move_direction):
                yield map_.move(i, map_[i])
    for stack in range(2, 9, 2):
        # Move out from stack
        if not map_.slot_empty(stack) and (top := map_.slot_top(stack)):
            yield map_.move(top, stack)


def find_cheapest_path(map_: Map):
    stack: List[Tuple[int, Map, List[Map]]] = [(0, map_, [map_])]
    seen_states = dict()
    # f = open('out.txt', 'w+')
    while len(stack) != 0:
        current_cost, current, path = heapq.heappop(stack)
        t = current.as_str
        if t in seen_states.keys() and seen_states[t] <= current_cost:
            continue
        # f.write(str(current) + '\n')
        seen_states[t] = current_cost
        if current.won:
            return current, current_cost, path
        for cost_, move in get_all_moves(current):
            heapq.heappush(stack, (current_cost + cost_, move, path + [move]))
    return None, math.inf


def part1():
    data = load_data()
    print(data)
    path, energy, steps = find_cheapest_path(data)
    # print('\n---------\n'.join([str(step) for step in steps]))
    print(energy)


def part2():
    data = load_data(2)
    print(data)
    path, energy, steps = find_cheapest_path(data)
    # print('\n---------\n'.join([str(step) for step in steps]))
    print(energy)


if __name__ == '__main__':
    part1()
    part2()
