from collections import defaultdict
import re

DAY_NUM = "15"


def hash_0(op: str):
    current_value = 0
    for char in op:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def part_2(ops: str):
    lens_map = defaultdict(dict)
    for line in ops:
        label = re.findall("[a-z]+", line)[0]
        opcode = re.findall('[^0-9a-zA-Z]+', line)[0]
        box = int(hash_0(label))

        if opcode == "-":
            lens_map[box].pop(label, None)
        else:
            val = int(line[-1])
            lens_map[box][label] = val

    focusing_powers = []
    for box, lenses in lens_map.items():
        for i, lens in enumerate(lenses.values()):
            focusing_powers.append((int(box) + 1) * (int(i) + 1) * int(lens))
    print(focusing_powers)
    return sum(focusing_powers)


def main(inputs):
    codes = inputs.split(",")
    hashes = [hash_0(x) for x in codes]
    print(f"P1: {sum(hashes)}")
    print(f"P2: {part_2(codes)}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = file.read().rstrip()
    main(inputs)
