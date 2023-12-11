from collections import defaultdict

import numpy as np

DAY_NUM = "10"

N = (0, -1)
S = (0, 1)
E = (1, 0)
W = (-1, 0)

conn_map = {
    "|": (N, S),
    "-": (E, W),
    "L": (N, E),
    "J": (N, W),
    "7": (S, W),
    "F": (S, E),
    ".": ()
}


def parse_input(inputs) -> [tuple, dict]:
    atlas = defaultdict(lambda: {})
    start = None
    for y in range(len(inputs)):
        for x in range(len(inputs[0])):
            match inputs[y][x]:
                case "S":
                    start = (x, y)
                    atlas[(x, y)] = "S"
                case ".":
                    pass
                case _:
                    atlas[(x, y)] = {tuple(sum(x) for x in zip((x, y), d)) for d in
                                     conn_map[inputs[y][x]]}
    return start, atlas, len(inputs), len(inputs[0])


def check_connection(map, i, j) -> [tuple, tuple]:
    if i in map[j]:
        return j,
    return False, False


def get_loop(map, start, direction):
    loop = [start]
    curr = start
    next = tuple(sum(x) for x in zip(curr, direction))

    while next != start:
        if map[next] == "S":
            return loop
        if curr not in map[next]:
            return False
        curr, next = next, (map[next] - {curr}).pop()
        loop.append(curr)
    return loop


def get_inner_volume(loop, y_len, x_len):
    from matplotlib import path
    pipe = path.Path(loop)
    tot = 0
    for y in range(y_len):
        for x in range(x_len):
            if (x, y) not in loop and pipe.contains_point((x, y)):
                tot += 1
    return tot


def main(inputs):
    start, pipe_map, x_len, y_len = parse_input(inputs)
    for direction in (N, E, S, W):
        if (loop := get_loop(pipe_map, start, direction)):
            break
    print(f"P1: {len(loop) // 2}")
    print(f"P2: {get_inner_volume(inputs, loop, x_len, y_len)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [list(x.rstrip()) for x in file.readlines()]
    main(inputs)
