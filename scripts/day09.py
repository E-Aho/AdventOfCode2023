DAY_NUM = "09"


def get_next(hist):
    if hist[0] == hist[-1]:
        return hist[0]
    deltas = [hist[i + 1] - hist[i] for i in range(len(hist) - 1)]
    return hist[-1] + get_next(deltas)


def main(inputs):
    # p1
    p1_outs = [get_next(h) for h in inputs]
    print(sum(p1_outs))

    # p2
    reversed_inputs = [list(reversed(h)) for h in inputs]
    p2_outs = [get_next(h) for h in reversed_inputs]
    print(sum(p2_outs))


if __name__ == "__main__":
    with open(f"inputs/{DAY_NUM}/input.txt", "r") as file:
        inputs = [list(map(int, x.rstrip().split())) for x in file.readlines()]
    main(inputs)
