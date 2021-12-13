from collections import deque
from functools import reduce

brackets_map = {')': '(', ']': '[', '>': '<', '}': '{'}

def part1():
    with open('input.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    score_map = {')': 3, ']': 57, '}': 1197, '>': 25137}
    score = 0
    for line in lines:
        stack = deque()
        for c in line:
            if c in brackets_map.keys():
                if stack.pop() != brackets_map[c]:
                    score += score_map[c]
                    break
            else:
                stack.append(c)
    print(score)


def part2():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    score_map = {'(': 1, '[': 2, '{': 3, '<': 4}
    scores = []
    for line in lines:
        stack = deque()
        invalid = False
        for c in line:
            if c in brackets_map.keys():
                if invalid := (stack.pop() != brackets_map[c]):
                    break
            elif c != '\n':
                stack.append(c)
        if not invalid:
            scores.append(reduce((lambda a, b: a * 5 + b), reversed(list(map(score_map.get, stack)))))
    print(sorted(scores)[len(scores) // 2])


if __name__ == '__main__':
    part1()
    part2()
