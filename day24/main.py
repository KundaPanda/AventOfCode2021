import math
from collections import OrderedDict
from dataclasses import dataclass, field
from itertools import count
from operator import add, eq, floordiv, mul, sub
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
class Range:
    start: float
    stop: float
    step: int = 1

    def __add__(self, other):
        return Range(max(self.start, other.start), min(self.stop, other.stop), max(self.step, other.step))

    def __iter__(self):
        i = self.start
        while i < self.stop:
            yield i
            i += self.step


@dataclass
class BinOp:
    left: str
    right: Union[int, str]
    _op: ClassVar[Callable[[int, int], int]] = field(init=False)
    _inverse: ClassVar[Callable[[int, int], Union[int, List[Range]]]] = field(init=False)

    def eval(self, mappings):
        mappings[self.left] = self._op(mappings.get(self.left, 0),
                                       mappings.get(self.right, 0) if isinstance(self.right, str) else self.right)

    def invert(self, mappings):
        mappings[self.left] = self._inverse(mappings.get(self.left, 0),
                                            mappings.get(self.right, 0) if isinstance(self.right, str) else self.right)


@dataclass
class InpOp:
    var: str

    def eval(self, mappings, value):
        mappings[self.var] = value


class AddOp(BinOp):
    _op = add
    _inverse = sub


class MulOp(BinOp):
    _op = mul
    _inverse = floordiv


class DivOp(BinOp):
    _op = floordiv

    @staticmethod
    def _inverse(a, b):
        return [Range(a * b, a * b + b)]


class ModOp(BinOp):
    _op = mod

    @staticmethod
    def _inverse(a, b):
        return count(a, b)


class EqOp(BinOp):
    _op = eq

    @staticmethod
    def _inverse(a, b):
        return b if a else [Range(-math.inf, b), Range(b + 1, math.inf)]


def load_data():
    operations = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            data = line.split()
            match data[0]:
                case 'inp':
                    operations.append(InpOp(data[1]))
                case 'add':
                    operations.append(AddOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]))
                case 'mul':
                    operations.append(MulOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]))
                case 'div':
                    operations.append(DivOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]))
                case 'mod':
                    operations.append(ModOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]))
                case 'eql':
                    operations.append(EqOp(data[1], int(data[2]) if data[2].isnumeric() else data[2]))
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


def apply_reverse(operations: List[Union[BinOp, InpOp]], mappings: dict):
    input_ = []
    for op in operations:
        if isinstance(op, InpOp):
            input_.append(mappings[op.var])
        else:
            op.invert(mappings)
    return reversed(input_)


def part1():
    data = load_data()
    print(data)
    result = apply(data, 13)
    print(result)
    result = apply_reverse(data, result.copy())
    print(result)


def part2():
    data = load_data()
    print(data)


if __name__ == '__main__':
    part1()
    part2()
