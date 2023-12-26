import itertools

import numpy as np

DAY_NUM = "19"


class Rule:
    def __init__(self, to, check: str = None, op: str = None, val: int = None):
        self.to = to
        self.check = check
        if check:
            self.check = check
            self.op = op
            self.val = val

    def __call__(self, part: dict):
        if not self.check:
            return self.to
        if self.op == "<":
            if part[self.check] < self.val:
                return self.to
        else:
            if part[self.check] > self.val:
                return self.to
        return False

    def __str__(self):
        if self.check:
            return f"{self.check}{self.op}{self.val}: {self.to}"
        return f"{self.to}"

    def __repr__(self):
        return self.__str__()


class Rules:
    def __init__(self, rules):
        self.rules = rules

    def __call__(self, part):
        for rule in self.rules:
            if (out := rule(part)):
                return out

    def handle_range(self, part_range):
        outs = []
        running_range = part_range
        for rule in self.rules:
            if not rule.check:
                outs.append((rule.to, running_range))
                break
            # split range
            c = rule.check
            if rule.op == "<":
                low, high = (
                    (running_range[c][0], rule.val-1),
                    (rule.val, running_range[c][1])
                )
                if low[1] >= low[0]:
                    new_range = running_range.copy()
                    new_range[c] = low
                    outs.append((rule.to, new_range))
                if high[1] >= high[0]:
                    running_range[c] = high
            else:  # >
                low, high = (
                    (running_range[c][0], rule.val),
                    (rule.val+1, running_range[c][1])
                )
                if high[1] >= high[0]:
                    new_range = running_range.copy()
                    new_range[c] = high
                    outs.append((rule.to, new_range))
                if low[1] >= low[0]:
                    running_range[c] = low
        return outs

    def __repr__(self):
        return str(self.rules)


class End:
    def __init__(self, name):
        self.name = name
        self.hold = []
        self.hold_ranges = []

    def __str__(self):
        return f"{self.name}: {self.hold}"

    def __call__(self, part):
        self.hold.append(part)
        return "END"

    def handle_range(self, range):
        self.hold_ranges.append(range)
        return "END"


def parse_rules(raw_rules):
    out_rules = {}

    out_rules["A"] = End("A")
    out_rules["R"] = End("R")

    for row in raw_rules:
        name, rules = row[:-1].split("{")
        _rules = []
        sub_rules = rules.split(",")
        for sub_rule in sub_rules:
            if ":" in sub_rule:
                _, to = sub_rule.split(":")
                p = sub_rule[0]
                op = sub_rule[1]
                n = int(_[2:])
                _rules.append(Rule(to, check=p, op=op, val=n))
            else:
                _rules.append(Rule(to=sub_rule))
        out_rules[name] = Rules(_rules)
    return out_rules


def parse_parts(raw_parts):
    out = []
    for p in raw_parts:
        digits = [int(x.split("=")[1]) for x in p[:-1].split(",")]
        out.append(
            {"x": digits[0],
             "m": digits[1],
             "a": digits[2],
             "s": digits[3]}
        )
    return out


def handle_rules(parts, rules):
    for part in parts:
        name = "in"
        while name != "END":
            rule = rules[name]
            name = rule(part)

    accepted = rules["A"]
    return sum([sum(x.values()) for x in accepted.hold])


def find_all_combinations(rules):
    splits = [("in", {
        _: (1, 4000) for _ in ["x", "m", "a", "s"]
    })]
    while splits:
        name, ranges = splits.pop()
        new_splits = rules[name].handle_range(ranges)
        if new_splits != "END":
            splits += new_splits

    running_tot = 0
    for ranges in rules["A"].hold_ranges:
        running_tot += np.prod([x[1] - x[0] + 1 for x in ranges.values()])

    return running_tot

def main(raw_rules, raw_parts):
    rules = parse_rules(raw_rules)
    parts = parse_parts(raw_parts)
    print(f"P1:{handle_rules(parts, rules)}")
    print(f"P2: {find_all_combinations(rules)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        p1, p2 = [x.rstrip().split("\n") for x in file.read().split("\n\n")]
    main(p1, p2)
