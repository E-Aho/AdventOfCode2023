DAY_NUM = "13"

import numpy as np


def parse_input(string_array):
    return np.array(
        [list(x) for x in string_array]
    )


def find_reflection(island, diff: int = 0):
    for c in range(len(island[0]) - 1):
        limit = min(c + 1, len(island[0]) - c - 1)
        left = np.flip(island[:, c - limit + 1: c + 1], axis=1)
        right = island[:, c+1: c+1+limit]
        if np.sum(left != right) == diff:
            return c+1

    for r in range(len(island)-1):
        limit = min(r+1, len(island) - r - 1)
        top = np.flip(island[r - limit + 1: r + 1], axis=0)
        btm = island[r+1: r+1+limit]
        if np.sum(top != btm) == diff:
            return (r+1) * 100


def main(inputs):
    arrays = [parse_input(x) for x in inputs]

    p1 = 0
    p2 = 0

    for island in arrays:
        p1 += find_reflection(island)
        p2 += find_reflection(island, diff=1)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.split("\n") for x in file.read().split(("\n\n"))]
    main(inputs)
