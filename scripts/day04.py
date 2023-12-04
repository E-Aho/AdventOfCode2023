DAY_NUM = "04"
from collections import deque

def parse_input(inputs):
    split = [x.split(":")[1] for x in inputs]
    digits = [
        [list(map(int, a.split())), list(map(int, b.split()))]
            for a, b in [
            x.split("|") for x in split
        ]
    ]
    return digits


def main(inputs):
    digits = parse_input(inputs)
    match_map = {}
    score = 0

    # p1
    for card in range(len(digits)):
        winners, ours = digits[card]
        intersection = set(winners).intersection(set(ours))
        if (matches := len(intersection)) >= 1:
            score += 2**(matches-1)
            match_map[card] = matches
    print(f"Part 1: {score}")

    # p2
    card_counts = {x: 1 for x in range(len(digits))}
    for card in card_counts.keys():
        matches = match_map.get(card, 0)
        held = card_counts[card]
        if matches:
            for j in range(card+1, card+matches+1):
                card_counts[j] += held
    print(f"Part 2: {sum(card_counts.values())}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.strip() for x in file.readlines()]
    main(inputs)
