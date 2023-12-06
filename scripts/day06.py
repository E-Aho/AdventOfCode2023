import numpy as np

DAY_NUM = "06"


def main(inputs):
    times = list(map(int, inputs[0].split()[1:]))
    distances = list(map(int, inputs[1].split()[1:]))

    def find_intersection(d, t):
        # just returns lower intersection
        lower = 0
        upper = (t // 2) + 1
        while (upper - lower) > 1:
            mid = (upper + lower + 1) // 2
            if mid * (t - mid) <= d:
                lower = mid
            else:
                upper = mid
        return upper

    def get_wins(d, t):
        low = find_intersection(d, t)
        high = t - low
        return high + 1 - low

    wins = [get_wins(distances[i], times[i]) for i in range(len(times))]
    print(f"Part 1: {np.prod(wins)}")

    real_time = int("".join(map(str, times)))
    real_dist = int("".join(map(str, distances)))

    print(f"Part 2: {get_wins(real_dist, real_time)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.rstrip() for x in file.readlines()]
    main(inputs)
