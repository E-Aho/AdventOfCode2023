from typing import List

DAY_NUM = "05"


def parse_inputs(inputs):
    output_dict = {}
    sections = [x.split("\n") for x in inputs.split("\n\n")]
    seeds = [int(x) for x in sections[0][0].split(" ")[1:]]
    for section in sections[1:]:
        sect_name = section[0].split(" ")[0]
        rows = [[int(x) for x in y.split(" ")] for y in section[1:]]
        output_dict[sect_name] = rows
    return seeds, output_dict


def get_out_from_almanac(number, ranges):
    for dest, source, length in ranges:
        x = number - source
        if 0 <= x < length:
            return dest + x
    return number


def get_new_ranges(input_ranges: List[tuple], layer_ranges):
    output_ranges = []

    for destination, source, length in layer_ranges:
        running_ranges = []
        for start, end in input_ranges:

            before = start, min(end, source)
            inner = max(start, source), min(source + length, end)
            after = max(source + length, start), end

            if before[1] > before[0]:
                running_ranges.append(before)
            if inner[1] > inner[0]:
                output_ranges.append([x - source + destination for x in inner])
            if after[1] > after[0]:
                running_ranges.append(after)

        # make new possibly cut ranges the ranges checked for next layer
        input_ranges = running_ranges
    return output_ranges + input_ranges


def main(inputs):
    seeds, almanac = parse_inputs(inputs)

    # p1
    locations = []
    for seed in seeds:
        running = seed
        for v in almanac.values():
            running = get_out_from_almanac(running, v)
        locations.append(running)

    # p2
    ranges = [(seeds[i], seeds[i] + seeds[i + 1] - 1)
              for i in range(0, len(seeds), 2)]

    for layer in almanac.values():
        ranges = get_new_ranges(ranges, layer)

    print(f"Part 1: {min(locations)}")
    print(f"Part 2: {min(r[0] for r in list(ranges))}")


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/example.txt", "r") as file:
        inputs = file.read()
    main(inputs)
