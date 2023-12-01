def get_result_from_clean_strings(clean_strings):
    int_strings = ["".join([char for char in s if char.isdigit()]) for s in clean_strings]
    return sum([int(x[0]+x[-1])for x in int_strings])


def part1(inputs):
    nums = get_result_from_clean_strings(inputs)
    return nums

def part2(inputs):
    """This is gross but does the job"""
    fixed_chars = [
        s
        .replace("one", "o1e")
        .replace("two", "t2o")
        .replace("three", "t3e")
        .replace("four", "f4r")
        .replace("five", "f5e")
        .replace("six", "s6x")
        .replace("eight", "e8t")
        .replace("seven", "s7n")
        .replace("eight", "e8t")
        .replace("nine", "n9e")
        for s in inputs
    ]

    return get_result_from_clean_strings(fixed_chars)


if __name__ == "__main__":
    DAY_NUM = "01"

    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = file.read().split()

    with open(f"inputs/{DAY_NUM}/example.txt", "r") as file:
        examples = file.read().split()

    print(f"part 1: {part1(inputs)}")
    print(f"part 2: {part2(inputs)}")