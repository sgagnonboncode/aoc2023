from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers
from math import lcm

INPUT_FILE = "input/day08/part1.txt"
# INPUT_FILE = "input/day08/example.txt"


def parse_map(lines: list[str]) -> dict[str, (str, str)]:
    # skip two first lines

    desert_map = {}
    for line in lines[2:]:
        lr_split = line.split("=")
        current = lr_split[0][0:3]
        intersection = lr_split[1].split(",")
        left = intersection[0][-3:]
        right = intersection[1][1:4]

        desert_map[current] = (left, right)

    return desert_map


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    lr_sequence = [c for c in lines[0]]
    desert_map = parse_map(lines)

    current = "AAA"
    next_step = 0
    steps_len = len(lr_sequence)

    while current != "ZZZ":
        left, right = desert_map[current]
        step = lr_sequence[next_step % steps_len]

        if step == "L":
            current = left
        else:
            current = right

        next_step += 1

    return next_step


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    lr_sequence = [c for c in lines[0]]
    desert_map = parse_map(lines)

    current_nodes = [k for k in desert_map.keys() if k[2] == "A"]

    # for each nodes, determine how many steps it takes to reach a node ending in Z
    nodes_distance = [0 for _ in range(0, len(current_nodes))]

    for i in range(0, len(current_nodes)):
        current = current_nodes[i]
        next_step = 0
        steps_len = len(lr_sequence)

        while current[2] != "Z":
            left, right = desert_map[current]
            step = lr_sequence[next_step % steps_len]

            if step == "L":
                current = left
            else:
                current = right

            next_step += 1

        nodes_distance[i] = next_step

    # answer is the least common denominator of all nodes distance for the pattern to repeat itself
    return lcm(*nodes_distance)
