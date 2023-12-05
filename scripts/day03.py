from typing import Tuple

import numpy as np

DAY_NUM = "03"


def parse_matrix(matrix) -> Tuple[dict, dict]:
    """
    Scans matrix once, returns indexes of starts + stops of numbers,
     as well as the locations of objects.
    """

    number_ranges = dict()
    char_map = {}
    x_max = len(matrix[0]) - 1
    for y in range(len(matrix)):
        num_start = None
        for x in range(len(matrix[0])):
            cur = matrix[y][x]

            if cur.isdigit():
                if not num_start:
                    num_start = (x, y)
                if x == x_max:
                    index_range = (num_start, (x, y))
                    number = int("".join(matrix[y][index_range[0][0]: index_range[1][0]
                                                                      + 1]))
                    number_ranges[index_range] = number
            else:
                if num_start:
                    number_ranges[(num_start, (x - 1, y))] = int("".join(
                        matrix[y][num_start[0]:x]
                    ))
                    num_start = None
                if not cur == ".":
                    char_map[(x, y)] = cur
    return number_ranges, char_map


def get_adjacent_ranges(start, end):
    """Gets all indexes adjacent to sequence.
    NB: Returns values that might be outside range of array.
    Not an issue, as we just don't track those indexes in future steps."""
    min_x, y = start
    max_x = end[0]

    outer = set([
        (x, y + j)
        for x in range(min_x - 1, max_x + 2)
        for j in (1, -1)
    ]).union({(min_x - 1, y), (max_x + 1, y)})

    return outer


def main(inputs):
    m = [list(s) for s in inputs]
    number_coords, symbols = parse_matrix(m)

    part_symbols = []
    gear_map = {coord: [] for coord, symbol in symbols.items() if symbol == "*"}

    for (start, end), number in number_coords.items():

        found_objects = set()
        adjacent_range = get_adjacent_ranges(start, end)

        for idx in adjacent_range:
            if idx in symbols:
                found_objects.add(symbols[idx])
                if symbols[idx] == "*":
                    gear_map[idx].append(number)

        if found_objects:
            part_symbols.append(number)

    gear_ratios = [np.prod(v) for v in gear_map.values() if len(v) == 2]

    print(f"part 1: {sum(part_symbols)}")
    print(f"part 2: {sum(gear_ratios)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = file.read().split()

    main(inputs)
