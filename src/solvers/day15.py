from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers, extract_real_numbers
from math import lcm
from colorama import Fore, Back, Style

INPUT_FILE = "input/day15/part1.txt"
# INPUT_FILE = "input/day15/example.txt"


def apply_HASH_algorithm(step: str) -> int:
    value = 0
    for c in step:
        value = value + ord(c)
        value *= 17
        value %= 256

    return value


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    sequence_steps = lines[0].split(",")
    HASHed_steps = [apply_HASH_algorithm(step) for step in sequence_steps]
    return sum(HASHed_steps)


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    sequence_steps = lines[0].split(",")

    boxes: list[list[(str, int)]] = []

    for i in range(0, 256):
        boxes.append([])

    for step in sequence_steps:
        # print("Step:",step)

        if step.endswith("-"):
            # remove lens at label
            label = step.split("-")[0]
            box_number = apply_HASH_algorithm(label)

            boxes[box_number] = [
                (t[0], t[1]) for t in boxes[box_number] if t[0] != label
            ]

        else:
            # add lens to box
            left_right = step.split("=")
            label = left_right[0]
            focus = int(left_right[1])
            box_number = apply_HASH_algorithm(label)

            found = False
            for j in range(0, len(boxes[box_number])):
                if boxes[box_number][j][0] == label:
                    found = True
                    boxes[box_number][j] = (label, focus)
                    break

            if not found:
                boxes[box_number].append((label, focus))

        # for b in range(0,len(boxes)):
        #     if len(boxes[b]) > 0:
        #         print("Box",b,":",boxes[b])

    total_focusing_power = 0
    for b in range(0, len(boxes)):
        box_focusing_power = b + 1

        for l in range(0, len(boxes[b])):
            slot_power = l + 1
            focal_length_power = boxes[b][l][1]
            total_focusing_power += box_focusing_power * slot_power * focal_length_power

    return total_focusing_power
