import heapq
import math
from collections import namedtuple

import numpy as np

DAY_NUM = "17"

State = namedtuple("State", "x y v n")


def find_best_route(array, max_straight, min_straight: int = None):
    queue = [(0, State(0, 0, None, 0))]
    visited = set()
    heatloss_map = {State(0, 0, None, 0): 0}
    while queue:
        heatloss, state = heapq.heappop(queue)

        if state in visited:
            continue

        visited.add(state)

        if (
                state.y + 1 == array.shape[1] and
                state.x + 1 == array.shape[0] and
                (min_straight is None or state.n >= min_straight)
        ):
            return heatloss_map[state]

        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if (-dx, -dy) == state.v:
                continue

            new_x, new_y = state.x + dx, state.y + dy

            if (
                    new_x < 0 or
                    new_x >= array.shape[0] or
                    new_y < 0 or
                    new_y >= array.shape[1]
            ):
                continue

            if (dx, dy) == state.v:
                new_n = state.n + 1
            else:
                new_n = 1
                if min_straight and state.v is not None and state.n < min_straight:
                    continue
            if new_n < max_straight:
                new_heatloss = heatloss + array[new_x][new_y]
                new_state = State(new_x, new_y, (dx, dy), new_n)
                if new_heatloss < heatloss_map.get(new_state, math.inf):
                    heatloss_map[new_state] = new_heatloss
                    heapq.heappush(queue, (new_heatloss, new_state))

def main(array):
    print(inputs)
    print(f"P1: {find_best_route(array, 3)}")
    print(f"P2: {find_best_route(array, 10, 4)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = np.array([list(map(int, list(y))) for y in [x.rstrip() for x in
                                                             file.readlines()]])
    main(inputs)
