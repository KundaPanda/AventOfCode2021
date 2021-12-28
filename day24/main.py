import math
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import singledispatch
from itertools import count
from operator import add, eq, floordiv, mul, sub
from pprint import pprint
from typing import Callable, ClassVar, List, Union


# @dataclass
# class Variable(abc.ABC):
#     @abc.abstractmethod
#     def eval(self, mappings):
#         raise NotImplemented
#
# class ConstVariable(Variable):
#     value: int
#
#     def eval(self, mappings):
#         return self.value
#
# class NamedVariable(Variable):
#     name: str
#
#     @abc.abstractmethod
#     def eval(self, mappings):
#         return mappings.get(self.name)

def mod(_, a, b):
    if a < 0:
        return -(a % b)
    return a % b


@dataclass
class BinOp:
    left: str
    right: Union[int, str]
    _op: ClassVar[Callable[[int, int], int]] = field(init=False)

    def eval(self, mappings):
        mappings[self.left] = self._op(mappings.get(self.left, 0),
                                       mappings.get(self.right, 0) if isinstance(self.right, str) else self.right)


@dataclass
class InpOp:
    var: str

    def eval(self, mappings, value):
        mappings[self.var] = value


class AddOp(BinOp):
    _op = add


class DivOp(BinOp):
    _op = floordiv


class MulOp(BinOp):
    _op = mul


class ModOp(BinOp):
    _op = mod


class EqOp(BinOp):
    _op = lambda _, a, b: int(eq(a, b))


def load_data():
    operations = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            data = line.split()
            operations.append({
                                  'inp': lambda: InpOp(data[1]),
                                  'add': lambda: AddOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]),
                                  'mul': lambda: MulOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]),
                                  'div': lambda: DivOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]),
                                  'mod': lambda: ModOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]),
                                  'eql': lambda: EqOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]),
                              }[data[0]]())
    return operations


def apply(operations: List[Union[BinOp, InpOp]], *input_):
    mappings = OrderedDict()
    input_idx = 0
    for op in operations:
        if isinstance(op, InpOp):
            op.eval(mappings, input_[input_idx])
            input_idx += 1
        else:
            op.eval(mappings)
    return mappings


def apply_reverse(operations: List[Union[BinOp, InpOp]], mappings: dict, idx=0):
    results = {}
    for i in range(idx, len(operations)):
        op = operations[i]
        if i < idx:
            continue
        if isinstance(op, InpOp):
            for i_ in range(1, 10):
                new_mappings = mappings.copy()
                op.eval(new_mappings, i_)
                res = apply_reverse(operations, new_mappings, i + 1)
                if 'z' in res:
                    results[str(i_)] = res
                elif res:
                    results.update((f'{i_}{k}', v) for k, v in res.items())
            return results
        op.eval(mappings)
    return mappings if mappings['z'] == 0 else {}


first_in = [1, 1, 1, 26, 26, 1, 1, 1, 26, 26, 26, 1, 26, 26]
second_in = [12, 12, 15, -8, -4, 15, 14, 14, -13, -3, -7, 10, -6, -8]
third_in = [1, 1, 16, 5, 9, 3, 2, 15, 5, 11, 7, 1, 10, 3]


def invert(i, z_prev, w):
    z_ = (z_prev - w - third_in[i])
    if z_ % 26 == 0:
        yield z_ // 26 * first_in[i]
    if w - second_in[i] in range(0, 26):  # z % 26 == w - second_in[i] -> w - second_in[i] in <0, 26)
        yield z_prev * first_in[i] + w - second_in[i]


def run_one(i, z, w):
    if (z % 26) + second_in[i] == w:
        z = z // first_in[i]
    else:
        z = (z * 26) // first_in[i]
        z = z + w + third_in[i]
    return z


"""
(z % 26) + s == w
z % 26 == s - w


z_prev = (z * 26) // f + w + t
z = (z_prev - w - t) // 26 * f
"""


def run(w):
    z = 0
    for i in range(14):
        wi = w // (10 ** (13 - i)) % 10  # helper for dividing numbers by powers of 10
        z = run_one(i, z, wi)
    return z


def run_original(w):
    x, y, z = 0, 0, 0
    for i in range(14):
        wi = w // (10 ** (13 - i)) % 10
        x = int(((z % 26) + second_in[i]) != wi)  # 0 or 1
        y = (25 * x) + 1  # 1 or 26
        z = (z * y) // first_in[i]
        y = (wi + third_in[i]) * x
        z += y
    return z


def get_accepted_numbers():
    z_values = {0}
    results = {0: {tuple()}}
    for i in range(13, -1, -1):
        z_values_prev = set({})
        for z in z_values:
            for w in range(1, 10):
                for z_prev in invert(i, z, w):
                    z_values_prev.add(z_prev)
                    if z_prev not in results:
                        results[z_prev] = set()
                    for sub_result in results[z]:
                        results[z_prev].add((w, *sub_result))
        z_values = z_values_prev
    return {int(''.join(map(str, result))) for k, v in results.items() for result in v if len(result) == 14}


def part1():
    results = get_accepted_numbers()
    print(max(results))


def part2():
    results = get_accepted_numbers()
    print(min(results))


if __name__ == '__main__':
    part1()
    part2()
