import numpy as np
import pandas as pd


def part1():
    array = np.genfromtxt('input.txt', dtype=int, delimiter=1)
    df = pd.DataFrame(array)
    v = ""
    for col in df.columns:
        v += str(df[col].mode()[0])
    gamma = int(v, 2)
    epsilon = int(v, 2) ^ 0xFFF
    print(epsilon * gamma)


def part2():
    array = np.genfromtxt('input.txt', dtype=int, delimiter=1)
    df = pd.DataFrame(array)
    oxygen = df.copy()
    co2 = df.copy()
    for bit in range(12):
        oxygen_mc = oxygen[bit].mode()
        oxygen_mc = oxygen_mc[1] if len(oxygen_mc) == 2 else oxygen_mc[0]
        oxygen = oxygen[oxygen[bit] == oxygen_mc]

        if len(co2) != 1:
            co2_mc = co2[bit].mode()
            co2_mc = co2_mc[1] if len(co2_mc) == 2 else co2_mc[0]
            co2 = co2[co2[bit] != co2_mc]
    co2_num = int(''.join(str(v) for v in co2.head(1).values[0]), 2)
    oxygen_num = int(''.join(str(v) for v in oxygen.head(1).values[0]), 2)
    print(co2_num * oxygen_num)


if __name__ == '__main__':
    # part1()
    part2()
