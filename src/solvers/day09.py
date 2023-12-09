from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers
from math import lcm

INPUT_FILE = "input/day09/part1.txt"
# INPUT_FILE = "input/day09/example.txt"


def parse_line(line: str) -> list[int]:
    return [int(n) for n in line.split()]


def derive_difference_sequence(sequence: list[int]) -> list[int]:
    diff_seq = []

    for i in range(0, len(sequence) - 1):
        diff_seq.append(sequence[i + 1] - sequence[i])

    return diff_seq


def predict_values(sequence: list[int]) -> list[int]:
    differences_stack: list[list[int]] = [sequence]

    current = sequence
    while True:
        differences = derive_difference_sequence(current)
        differences_stack.append(differences)

        if all(x == 0 for x in differences):
            break
        current = differences

    differences_stack[len(differences_stack) - 1].append(0)

    for j in range(len(differences_stack) - 2, -1, -1):
        next_value = differences_stack[j + 1][-1] + differences_stack[j][-1]
        differences_stack[j].append(next_value)
        prev_value = -differences_stack[j + 1][0] + differences_stack[j][0]
        differences_stack[j].insert(0, prev_value)

    return differences_stack[0]


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    sequences = [parse_line(line) for line in lines]
    previsions = []

    for seq in sequences:
        predicted = predict_values(seq)[-1]
        previsions.append(predicted)

    return sum(previsions)


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    sequences = [parse_line(line) for line in lines]
    previsions = []

    for seq in sequences:
        predicted = predict_values(seq)[0]
        previsions.append(predicted)

    return sum(previsions)
