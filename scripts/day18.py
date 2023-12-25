import numpy as np

DAY_NUM = "18"


def parse_input(inputs):
    out = []
    for row in inputs:
        d, n, c = row.split(" ")
        colour = c.split("#")[1][:-1]
        out.append((d, int(n), colour))
    return out


def get_walls(steps):
    p1_start = (0, 0)
    p1_walls = [p1_start]
    p2_start = (0, 0)
    p2_walls = [p2_start]
    d_map = {
        "R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1),
        "0": (1, 0),
        "1": (0, -1),
        "2": (-1, 0),
        "3": (0, 1)
    }

    for step in steps:
        # p1
        direction, number, colour = step
        vec = d_map[direction]
        end = tuple(np.add(p1_start, number * np.array(vec)))
        p1_walls.append(end)
        p1_start = end

        # p2
        vec = d_map[colour[-1]]
        n = int(colour[:5], 16)
        p2_end = tuple(np.add(p2_start, n * np.array(vec)))
        p2_walls.append(p2_end)
        p2_start = p2_end

    return p1_walls, p2_walls


def get_area(loop: list[tuple, tuple]):
    area = 0
    perimeter = 0

    # use pick's theorem
    for i in range(len(loop) - 1):
        area += loop[i][1] * (loop[i + 1][0] - loop[i - 1][0])
        perimeter += abs(loop[i][0] - loop[i + 1][0]) + abs(loop[i][1] - loop[i + 1][1])
    return area // 2 + perimeter // 2 + 1


def main(inputs):
    p1_walls, p2_walls = get_walls(parse_input(inputs))
    p1 = get_area(p1_walls)
    print(p1)
    p2 = get_area(p2_walls)
    print(p2)


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.rstrip() for x in file.readlines()]
    main(inputs)
