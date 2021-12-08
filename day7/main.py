import numpy as np


def task(cost_fn):
    with open('input.txt', 'r') as f:
        s = np.array(f.readline().strip().split(','), dtype=np.int32)

    mean = np.rint(np.mean(s))

    best = cost_fn(s, mean)
    best_i = best - 1
    best_d = best - 1
    for i in range(1, len(s)):
        if best_i <= best:
            best_i = cost_fn(s, mean + i)
        if best_d <= best:
            best_d = cost_fn(s, mean - i)
        best = min(best, best_d, best_i)
    print(best)


def part1():
    def cost(nums, mean_):
        return np.sum(np.absolute(nums - np.full((len(nums),), mean_)))

    task(cost)


def part2():
    def cost(nums, mean_):
        return np.sum(
            np.vectorize(lambda n: (n * (n + 1) / 2))(np.absolute(nums - np.full((len(nums),), mean_, dtype=np.int32))))

    task(cost)


if __name__ == '__main__':
    part1()
    part2()
