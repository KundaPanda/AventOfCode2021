import re
from collections import defaultdict
from dataclasses import dataclass, field
from decimal import Decimal
from functools import cached_property, lru_cache
from math import sqrt
from typing import Dict, Iterable, NamedTuple, Optional, Set

import numpy as np


class Position(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def from_array(array: Iterable[int]):
        return Position(*array)

    def distance(self, to: 'Position') -> Decimal:
        return Decimal(sqrt(sum(map(lambda n: pow(n, 2), [self.x - to.x, self.y - to.y, self.z - to.z])))) \
            .quantize(Decimal('.001'))

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass
class Scanner:
    id: int
    position: Optional[Position] = None
    beacons: Set[Position] = field(default_factory=lambda: set())
    distances: Dict[Position, Dict[Position, Decimal]] = \
        field(default_factory=lambda: defaultdict(lambda: defaultdict(Decimal)))
    # nearby: Dict['Scanner', Set[Position]] = field(default_factory=lambda: defaultdict(lambda: set()))
    nearby: Dict['Scanner', Dict[Position, Position]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(Position)))
    _transformation_matrix: np.ndarray = np.identity(3)
    transformation_origin: 'Scanner' = None

    def __str__(self):
        return f'Scanner {self.id}{" " + str(self.position) if self.position else ""} - ' \
               f'nearby [{",".join([str(s.id) for s in self.nearby.keys()])}]'

    def __hash__(self):
        return hash(self.id)

    @cached_property
    def beacons_array(self):
        return np.matmul(self.transformation_matrix, (points_to_array(self.beacons)).T).T + self.position.to_numpy().T

    @cached_property
    def transformation_matrix(self):
        return np.matmul(self.transformation_origin.transformation_matrix, self._transformation_matrix) \
            if self.transformation_origin \
            else self._transformation_matrix

    def set_transformation_matrix(self, matrix: np.ndarray):
        self._transformation_matrix = matrix[:]

    @cached_property
    def all_distances(self) -> Set[Position]:
        distances = set()
        for values in self.distances.values():
            distances.update(values.values())
        return distances

    @lru_cache
    def get_point_by_distance(self, distance: Decimal):
        for source, values in self.distances.items():
            for target, distance_ in values.items():
                if distance_ == distance:
                    return target
        return None

    def get_distances(self):
        for beacon in self.beacons:
            for target in self.beacons - {beacon}:
                self.distances[beacon][target] = beacon.distance(target)


def points_to_array(points: Iterable[Position]):
    return np.array([point.to_numpy() for point in points])


def find_nearby_scanners(scanners: Dict[int, Scanner]):
    scanned = set()
    for scanner in scanners.values():
        for target in set(scanners.values()) - {scanner}:
            if (scanner, target) in scanned:
                continue
            for pos, distances in scanner.distances.items():
                for target_pos, target_distances in target.distances.items():
                    common_distances = set(distances.values()).intersection(set(target_distances.values()))
                    if len(common_distances) >= 11:
                        scanner.nearby[target][pos] = target_pos
                        target.nearby[scanner][target_pos] = pos
                        break
            scanned.update([(scanner, target), (target, scanner)])


def localize_nearby_scanners(scanner: Scanner):
    if not scanner.transformation_origin and scanner.id != 0:
        return
    for target, nearby_points in scanner.nearby.items():
        if target.transformation_origin or target.id == 0:
            continue
        local_points = points_to_array(nearby_points.keys())
        target_points = points_to_array(nearby_points.values())
        local_diffs = (local_points - local_points[0])[1:].T
        target_diffs = (target_points - target_points[0])[1:].T
        transformation_matrix = np.zeros((3, 3))
        for axis in range(local_diffs.shape[0]):
            remote_axis = np.where((np.abs(target_diffs) == np.abs(local_diffs[axis])).all(axis=1))[0][0]
            transformation_matrix[axis][remote_axis] = 1 if local_diffs[axis][0] == target_diffs[remote_axis][0] else -1
        target.transformation_origin = scanner
        target.set_transformation_matrix(transformation_matrix)
        position = np.matmul(scanner.transformation_matrix,
                             (local_points.T - np.matmul(transformation_matrix, target_points.T))).T[0]
        target.position = scanner.position + Position.from_array(position)
        localize_nearby_scanners(target)


def load_data():
    with open('input.txt', 'r') as f:
        data = {}
        scanner: Scanner
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if scanner_id := re.findall(r'--- scanner (\d+) ---', line):
                scanner = Scanner(int(scanner_id[0]))
                if scanner.id == 0:
                    scanner.position = Position(0, 0, 0)
                data[scanner.id] = scanner
                continue
            position = line.split(',')
            scanner.beacons.add(Position(*list(map(int, position))))
    for scanner in data.values():
        scanner.get_distances()
    find_nearby_scanners(data)
    localize_nearby_scanners(data[0])
    return data


data = load_data()


def part1():
    beacons = set()
    for scanner in data.values():
        beacons.update([tuple(beacon) for beacon in scanner.beacons_array])
    print(len(beacons))


def part2():
    max_distance = 0
    positions = np.array([scanner.position.to_numpy() for scanner in data.values()])
    for position in positions:
        max_distance = max(max_distance, np.sum(np.abs(positions - position), axis=1).max(initial=0))
    print(max_distance)


if __name__ == '__main__':
    part1()
    part2()
