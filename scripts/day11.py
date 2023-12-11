from bisect import bisect
from itertools import combinations

DAY_NUM = "11"


def get_raw_galaxies(inputs):
    galaxies = []
    xs, ys, = set(), set()
    for y, line in enumerate(inputs):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.append((x, y))
                xs.add(x)
                ys.add(y)
    empty_x = sorted(list(set(range(len(inputs[0]))) - xs))
    empty_y = sorted(list(set(range(len(inputs))) - ys))
    return galaxies, empty_x, empty_y


def expand_galaxies(galaxies, empty_xs, empty_ys, expansion_factor: int = 1):
    # expand based on bisected index into sorted empty space arrays
    fixed_galaxies = {
        (
            x + bisect(empty_xs, x) * (expansion_factor - 1),
            y + bisect(empty_ys, y) * (expansion_factor - 1)
        ) for x, y in galaxies
    }
    return fixed_galaxies


def manhattan_dist(i, j):
    return abs(i[0] - j[0]) + abs(i[1] - j[1])


def main(inputs):
    raw_galaxies, empty_x, empty_y = get_raw_galaxies(inputs)
    for part, factor in [("P1", 2), ("P2", 1000000)]:
        expanded_galaxies = expand_galaxies(raw_galaxies, empty_x, empty_y, factor)
        total_dist = 0
        for i, j in combinations(expanded_galaxies, 2):
            total_dist += manhattan_dist(i, j)

        print(f"{part}: {total_dist}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [list(x.rstrip()) for x in file.readlines()]
    main(inputs)
