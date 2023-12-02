DAY_NUM = "02"
from collections import defaultdict
import numpy as np

def parse_games(inputs):
    games = [i.split(";") for i in [j.split(":")[1] for j in inputs]]

    def parse_reveal_group(reveal_group: str):
        d = defaultdict(int)
        for pair in reveal_group.split(","):
            count, color = pair.strip().split(" ")
            d[color] += int(count)
        return d

    game_dicts = [[parse_reveal_group(r) for r in game] for game in games]
    return game_dicts



def part1(inputs):

    game_dicts = parse_games(inputs)

    valid_count = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    def is_valid_reveal(reveal, valid_counts):
        for color, count in valid_counts.items():
            if reveal[color] > count:
                return False
        return True


    def is_valid_game(game):
        for reveal in game:
            if not is_valid_reveal(reveal, valid_count):
                return False
        return True

    valid_ids = [id+1 for id, game in enumerate(game_dicts) if is_valid_game(game)]
    return sum(valid_ids)


def part2(inputs):
    def get_optimal_power(game):
        running_dict = {}
        for reveal in game:
            for color, count in reveal.items():
                if color not in running_dict:
                    running_dict[color] = count
                running_dict[color] = max(count, running_dict[color])

        power = np.prod(list(running_dict.values()))
        return power

    game_dicts = parse_games(inputs)
    return sum([get_optimal_power(game) for game in game_dicts])


if __name__ == "__main__":

    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.rstrip() for x in file.readlines()]

    print(f"part 1: {part1(inputs)}")
    print(f"part 2: {part2(inputs)}")

