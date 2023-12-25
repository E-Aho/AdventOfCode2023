from collections import defaultdict
from typing import List

import numpy as np

DAY_NUM = "16"


def is_valid(grid, pos):
    return 0 <= pos[0] < grid.shape[1] and 0 <= pos[1] < grid.shape[0]


def calculate_laser(grid: np.array, pos: tuple, vec: tuple) -> List[tuple[tuple,
tuple]]:
    new_p = tuple(np.add(pos, vec))
    if not is_valid(grid, new_p):
        return []
    c = grid[new_p[1], new_p[0]]
    match c:
        case ".":
            return [(new_p, vec)]
        case "/":
            return [(new_p, (-vec[1], -vec[0]))]
        case "\\":
            return [(new_p, (vec[1], vec[0]))]
        case "-":
            if vec[1] == 0:
                return [(new_p, vec)]
            return [(new_p, (1, 0)), (new_p, (-1, 0))]
        case "|":
            if vec[0] == 0:
                return [(new_p, vec)]
            return [(new_p, (0, 1)), (new_p, (0, -1))]
    print("Oops")


def energize(input_grid, starts):
    visited = defaultdict(set)

    current_lasers = starts
    while current_lasers:
        p, v = current_lasers.pop()
        for new_p, new_v in calculate_laser(input_grid, p, v):
            if new_v not in visited[new_p]:
                visited[new_p].add(new_v)
                current_lasers.append((new_p, new_v))
    return len(visited.keys())


def main(input_grid):
    print(array)
    print(f"Part 1:{energize(input_grid, [((-1, 0), (1, 0))])}")
    resultant_energies = []
    for y in range(0, input_grid.shape[1]):
        resultant_energies.append(
            energize(input_grid, [((-1, y), (1, 0))])
        )
        resultant_energies.append(
            energize(input_grid, [((input_grid.shape[0], y), (-1, 0))])
        )
    for x in range(0, input_grid.shape[0]):
        resultant_energies.append(
            energize(input_grid, [((x, -1), (0, 1))])
        )
        resultant_energies.append(
            energize(input_grid, [((x, input_grid.shape[1]), (0, -1))])
        )

    print(f"P2: {max(resultant_energies)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        array = np.array([list(x.rstrip()) for x in file.readlines()])
    main(array)
