from collections import Counter

DAY_NUM = "07"

rank_map = {x: i for i, x in enumerate(([str(x) for x in range(2, 10)] + ["T", "J", "Q", "K", "A"]))}
joker_rank_map = rank_map.copy()
joker_rank_map["J"] = -1

strength_map = {
    "5_kind": 6,
    "4_kind": 5,
    "full_house": 4,
    "3_kind": 3,
    "2_pair": 2,
    "pair": 1,
    "high": 0
}


class Hand:

    def __init__(self, cards, score, jokers=False):
        self.cards = cards
        self.score = score
        self.jokers = jokers
        self.strength = None
        self.set_strength(jokers)

    def set_strength(self, jokers=False):
        card_count = Counter(self.cards)
        hand_score = 0

        # apply jokers if needed
        if jokers and "J" in card_count:
            joker_count = card_count["J"]
            if card_count.most_common()[0][0] == "J":
                if card_count.most_common()[0][1] == 5:
                    # edge case: all jokers
                    self.strength = strength_map["5_kind"], [joker_rank_map[x] for x in self.cards]
                    return
                else:
                    card_count[card_count.most_common()[1][0]] += joker_count
                    card_count["J"] = 0
            else:
                card_count[card_count.most_common()[0][0]] += card_count["J"]
                card_count["J"] = 0

        # find strength of hand
        max_count = card_count.most_common()[0][1]
        match max_count:
            case 5:
                hand_score = strength_map["5_kind"]
            case 4:
                hand_score = strength_map["4_kind"]
            case 3:
                if card_count.most_common(2)[1][1] == 2:
                    hand_score = strength_map["full_house"]
                else:
                    hand_score = strength_map["3_kind"]
            case 2:
                if card_count.most_common(2)[1][1] == 2:
                    hand_score = strength_map["2_pair"]
                else:
                    hand_score = strength_map["pair"]
            case 1:
                hand_score = strength_map["high"]

        if not jokers:
            vals = [rank_map[x] for x in self.cards]
        else:
            vals = [joker_rank_map[x] for x in self.cards]

        self.strength = hand_score, vals

    def __eq__(self, other):
        return self.strength == other.strength

    def __lt__(self, other):
        if self == other:
            return False

        if self.strength[0] != other.strength[0]:
            return self.strength[0] < other.strength[0]

        # same type of hand, need to score on cards in hand
        ours, theirs = self.strength[1], other.strength[1]
        for i in range(len(self.cards)):
            if ours[i] != theirs[i]:
                return ours < theirs


def main(inputs):
    hands = [Hand(cards, int(score)) for cards, score in [s.split(" ") for s in inputs]]
    sorted_hands = sorted(hands)

    # p1
    winnings = sum([(i+1) * hand.score for i, hand in enumerate(sorted_hands)])
    print(f"P1: {winnings}")

    # p2
    for hand in hands:
        hand.set_strength(jokers=True)
    sorted_hands = sorted(hands)
    winnings = sum([(i+1) * hand.score for i, hand in enumerate(sorted_hands)])
    print(f"P2: {winnings}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.rstrip() for x in file.readlines()]

    main(inputs)
