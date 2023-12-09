from collections import defaultdict

import numpy as np

DAY_NUM = "08"


def parse_inputs(inputs):
    directions = inputs[0]
    raw_nodes = inputs[2:]
    out = {}
    for n in raw_nodes:
        name, _, l, r = n.replace("(", "").replace(")", "").replace(",", "").split(" ")
        out[name] = (l, r)
    return directions, out


def get_end_timings(directions, nodes, start):
    # returns (start of loop, loop length), and times all endings are hit during loop
    total_steps = 0
    end_idx_map = defaultdict(list)
    current = start
    while True:
        if directions[total_steps % len(directions)] == "L":
            total_steps += 1
            current = nodes[current][0]
        else:
            total_steps += 1
            current = nodes[current][1]

        if current[2] == "Z":

            for e in end_idx_map[current]:
                if e % len(directions) == total_steps % len(directions):
                    loop_length = total_steps - e
                    return (e, loop_length), end_idx_map

            end_idx_map[current].append(total_steps)


def main(parsed_inputs):
    directions, nodes = parsed_inputs
    curr = "AAA"
    end = "ZZZ"
    steps_taken = 0

    # p1
    while curr != end:
        d = directions[steps_taken % len(directions)]
        if d == "L":
            curr = nodes[curr][0]
            steps_taken += 1
        else:
            curr = nodes[curr][1]
            steps_taken += 1
    print(f"Part 1: {steps_taken}")

    # p2
    # luckily, loops all start at 0 and have only one end
    # can just do lcm for length of loop, no need to do anything complex
    curs = set(n for n in nodes.keys() if n[2] == "A")

    loops = []
    for c in curs:
        loop_timings, end_timings = get_end_timings(directions, nodes, c)
        loops.append(loop_timings[0])

    print(f"Part 2: {np.lcm.reduce(loops)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.rstrip() for x in file.readlines()]
    main(parse_inputs(inputs))
