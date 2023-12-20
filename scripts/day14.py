import numpy as np

DAY_NUM = "14"


def get_load(array):
    round_rocks = np.argwhere(np.isin(array, "O"))
    return sum([len(array[0]) - x[0] for x in round_rocks])


def tilt_rocks(array, direction="N") -> np.array:
    # rotate array to allow us to tilt in any direction with same logic

    rot_map = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": -1
    }

    array = np.rot90(array, k=rot_map[direction])

    # do tilt
    for column in range(len(array[0])):
        c = array[:, column]
        col = "".join(c).split("#")
        out = "#".join(["".join(sorted(x, reverse=True)) for x in col])
        array[:, column] = list(out)

    # rotate back
    out = np.rot90(array, k=-1 * rot_map[direction])
    return out


def find_array_after_cycles(initial_array, count_cycles: int = 1000000000):
    running_arr = initial_array
    cache = {}

    for cycle in range(count_cycles):
        # checks until we hit loops, and breaks to the state equivalent to solution
        hash_key = running_arr.tostring()
        if hash_key in cache:
            start = cache[hash_key][1]
            loop_len = cycle - start
            remainder = (count_cycles - cycle) % loop_len
            if remainder == 0:  # equivalent to the solution at end of all cycles
                return running_arr
            running_arr = cache[hash_key][0]
        else:
            for r in ["N", "W", "S", "E"]:
                running_arr = tilt_rocks(running_arr, r)
            cache[hash_key] = (running_arr.copy(), cycle)


def main(array):
    tilted = tilt_rocks(array)
    load = get_load(tilted)
    print(f"P1: {load}")

    print(f"P2: {get_load(find_array_after_cycles(array))}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        array = np.array([list(x.rstrip()) for x in file.readlines()])
    main(array)
