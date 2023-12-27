import numpy as np

DAY_NUM = "20"

from collections import namedtuple, defaultdict

class Pulse:
    def __init__(self, by, s):
        self.by = by
        self.s = s


class FlipFlop:
    def __init__(self, name, to, conn):
        self.s = False
        self.to = to
        self.conn = conn
        self.name = name

    def __call__(self, p: Pulse):
        if not p.s:
            self.s = not self.s
            return [(t, Pulse(self.name, self.s)) for t in self.to]
        return None

    def __str__(self):
        return f"%{self.name}: from={self.conn}, to={self.to}, state={self.s}"

    def __repr__(self):
        return self.__str__()


class Conjunction:
    def __init__(self, name, to, conn):
        self.s = {c: False for c in conn}
        self.to = to
        self.conn = conn
        self.name = name

    def __call__(self, p: Pulse):
        self.s[p.by] = p.s
        all_high = all(self.s.values())
        return [(t, Pulse(self.name, not all_high)) for t in self.to]

    def __str__(self):
        return f"&{self.name}: from={self.conn}, to={self.to}, state={str(self.s)}"

    def __repr__(self):
        return self.__str__()


class Broadcaster:
    def __init__(self, to):
        self.to = to
        self.name = "broadcaster"

    def __call__(self, p: Pulse):
        return [(t, Pulse(self.name, p.s)) for t in self.to]

    def __str__(self):
        return f"Broadcaster: {self.to}"

    def __repr__(self):
        return self.__str__()


def parse_input(inputs):
    conn_map = defaultdict(lambda: {"name": None, "conn": [], "to": [], "type": None})

    for row in inputs:
        if row[0] == "b":
            # broadcaster
            conn_to = row.replace(" ", "").split("->")[1].split(",")
            conn_map["broadcaster"] = {"name": "broadcaster", "to": conn_to, "type":
                "b"}
            for c in conn_to:
                conn_map[c]["conn"].append("broadcaster")
        else:
            detail, to = row.replace(" ", "").split("->")
            module_name = detail[1:]
            outs = to.split(",")
            for c in outs:
                conn_map[c]["conn"].append(module_name)
            conn_map[module_name]["name"] = module_name
            conn_map[module_name]["to"] = outs
            conn_map[module_name]["type"] = detail[0]

    out_modules = {}
    for name, module in conn_map.items():
        match module["type"]:
            case "&":
                out_modules[name] = Conjunction(name=module["name"], conn=module[
                    "conn"], to=module["to"])
            case "%":
                out_modules[name] = FlipFlop(name=module["name"], conn=module[
                    "conn"], to=module["to"])
            case "b":
                out_modules[name] = Broadcaster(to=module["to"])
    return out_modules


def push_button(modules):
    pulses = [("broadcaster", Pulse("button", False))]
    lows = 0
    highs = 0
    while pulses:
        to, p = pulses.pop(0)
        if p.s:
            highs += 1
        else:
            lows += 1
        if to not in modules:
            continue
        return_pulses = modules[to](p)
        if return_pulses:
            pulses += return_pulses
    return modules, highs, lows

def push_till_rx_low(modules):
    presses = 0
    connected_to_rx = [name for name, mod in modules.items() if "rx" in mod.to]
    # should be a single conjunction module
    adjacencies = {
        name: [] for name, mod in modules.items()
        if connected_to_rx[0] in mod.to
    }

    # conjunction module will release Low if all inputs are High
    # having checked, a false signal always occurs in the press after a true signal
    # for each of the connected modules
    # and the signals are evenly repeated for each module, so just need lcm
    while True:
        presses += 1
        pulses = [("broadcaster", Pulse("button", False))]
        while pulses:
            to, p = pulses.pop(0)
            if to == connected_to_rx[0] and p.s:
                adjacencies[p.by].append(presses)
            if to == "rx":
                continue
            return_pulses = modules[to](p)
            if return_pulses:
                pulses += return_pulses
        if all(
            len(mod) > 0 for mod in adjacencies.values()
        ):
            return np.lcm.reduce([mod[0] for mod in adjacencies.values()])



def push_button_n_times(modules, n):
    highs, lows = 0, 0
    for _ in range(n):
        modules, h, l = push_button(modules)
        highs += h
        lows += l
    return highs, lows

def main(inputs):
    modules = parse_input(inputs)
    modules, highs, lows = push_button(modules)
    print(f"P1: {np.prod(push_button_n_times(modules, 1000))}")
    print(f"P2: {push_till_rx_low(parse_input(inputs))}")

if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [x.rstrip() for x in file.readlines()]
    main(inputs)
