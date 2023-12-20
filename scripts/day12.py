import functools
DAY_NUM = 12

def parse_inputs(inputs):
    springs, groups = [], []
    for row in inputs:
        _x, _s = row.split(" ")
        groups.append(tuple(map(int, _s.split(","))))
        springs.append(_x)
    return springs, groups


@functools.cache
def find_arrangements(spring, group):
    # quick outs
    if len(group) == 0:
        return int("#" not in spring)
    if sum(group) > len(spring):
        return 0
    if spring[0] == ".":
        return find_arrangements(spring[1:], group)

    running_sum = 0

    # can we make a group from next tile?
    if spring[0] == "?":
        running_sum += find_arrangements(spring[1:], group)

    # can we make a group from this tile?
    group_can_have_ending = True if len(spring) == group[0] else spring[group[0]] in [".", "?"]
    if all(char != "." for char in spring[:group[0]]) and group_can_have_ending:
        running_sum += find_arrangements(spring[(group[0]+1):], group[1:])

    return running_sum


def main(inputs):
    springs, groups = parse_inputs(inputs)

    p1 = []
    p2 = []

    for spring, group in zip(springs, groups):
        # p1
        p1.append(find_arrangements(spring, group))

        # p2
        new_spring = "?".join([spring] * 5)
        new_group = group * 5
        p2.append(find_arrangements(new_spring, new_group))
    print(f"Part 1: {sum(p1)}")
    print(f"Part 2: {sum(p2)}")

if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/example.txt", "r") as file:
        inputs = [x.rstrip() for x in file.readlines()]
    main(inputs)
