from dataclasses import dataclass
from typing import Dict, List, Tuple, Union


@dataclass
class Field:
    value: int
    marked: bool = False


def load_board(lines, idx):
    return [[Field(value=int(number)) for number in line.strip().split()] for line in lines[idx:idx + 6]]


def check_win(board, x, y):
    win = True
    for xc in range(0, 5):
        if not board[y][xc].marked:
            win = False
            break
    if win:
        return True
    win = True
    for yc in range(0, 5):
        if not board[yc][x].marked:
            win = False
            break
    return win


def run_bingo(number, boards: Dict[int, List[Union[bool, List[List[Field]]]]], win_order: List[Tuple[int, int]]):
    is_win = False
    for num, (won, board) in boards.items():
        if won:
            continue
        for y, row in enumerate(board):
            for x, col in enumerate(row):
                if col.value == number:
                    col.marked = True
                    if check_win(board, x, y):
                        value = 0
                        for yr in range(5):
                            for xr in range(5):
                                if not board[yr][xr].marked:
                                    value += board[yr][xr].value
                        value *= number
                        # print(f'Final score {value} of board {num}')
                        boards[num][0] = True
                        win_order.append((num, value))
                        is_win = True
    return is_win


def task1():
    with open('input.txt', 'r') as f:
        numbers = f.readline().split(",")
        lines = f.readlines()
    boards = {}
    i = 1
    while i < len(lines):
        boards[i // 6] = [False, load_board(lines, i)]
        i += 6
    win_order = []
    for number in numbers:
        if run_bingo(int(number), boards, win_order):
            print(win_order[0])
            return


def task2():
    with open('input.txt', 'r') as f:
        numbers = f.readline().split(",")
        lines = f.readlines()
    boards = {}
    i = 1
    while i < len(lines):
        boards[i // 6] = [False, load_board(lines, i)]
        i += 6
    win_order = []
    for number in numbers:
        run_bingo(int(number), boards, win_order)
    print(win_order[-1])


if __name__ == '__main__':
    task1()
    task2()
