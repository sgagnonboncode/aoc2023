from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers


def schematic_special_character(char: str) -> bool:
    return not char.isdigit() and char != "."


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines("input/day03/part1.txt")]
    # lines = [ line.strip()  for line in read_lines("input/day03/example.txt")]

    max_y = len(lines)
    max_x = len(lines[0])

    accumulator = 0
    special_neighbours = 0
    valid = []

    for j in range(0, max_y):
        for i in range(0, max_x):
            char = lines[j][i]
            # print(char, end="")

            if char.isdigit():
                accumulator *= 10
                accumulator += int(char)

                # verify neighbours
                if i > 0 and j > 0:
                    top_left = lines[j - 1][i - 1]
                    if schematic_special_character(top_left):
                        special_neighbours += 1
                if j > 0:
                    top = lines[j - 1][i]
                    if schematic_special_character(top):
                        special_neighbours += 1
                if i < max_x - 1 and j > 0:
                    top_right = lines[j - 1][i + 1]
                    if schematic_special_character(top_right):
                        special_neighbours += 1

                if i > 0:
                    left = lines[j][i - 1]
                    if schematic_special_character(left):
                        special_neighbours += 1

                if i < max_x - 1:
                    right = lines[j][i + 1]
                    if schematic_special_character(right):
                        special_neighbours += 1

                if j < max_y - 1 and i > 0:
                    bottom_left = lines[j + 1][i - 1]
                    if schematic_special_character(bottom_left):
                        special_neighbours += 1

                if j < max_y - 1:
                    bottom = lines[j + 1][i]
                    if schematic_special_character(bottom):
                        special_neighbours += 1

                if j < max_y - 1 and i < max_x - 1:
                    bottom_right = lines[j + 1][i + 1]
                    if schematic_special_character(bottom_right):
                        special_neighbours += 1

            else:
                if special_neighbours > 0:
                    valid.append(accumulator)
                accumulator = 0
                special_neighbours = 0

        if accumulator > 0 and special_neighbours > 0:
            valid.append(accumulator)

        accumulator = 0
        special_neighbours = 0

        # print()

    # print(valid)

    return sum(valid)


def extract_neighbors(numbers: list[int, int], i, same_line: bool = False):
    neighbour_range = [-1, 1] if same_line else [-1, 0, 1]
    neighbours = []

    for index, number in numbers:
        number_size = len(str(number))

        for k in range(0, number_size):
            dist = i - (index + k)
            if dist in neighbour_range:
                neighbours.append(number)
                break
    return neighbours


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines("input/day03/part1.txt")]
    # lines = [ line.strip()  for line in read_lines("input/day03/example.txt")]

    numbers_map = [extract_numbers(line) for line in lines]

    max_y = len(lines)
    max_x = len(lines[0])

    gear_ratios = []

    for j in range(0, max_y):
        for i in range(0, max_x):
            char = lines[j][i]

            if char != "*":
                continue

            gear_factors = []

            if j > 0:
                gear_factors.extend(extract_neighbors(numbers_map[j - 1], i))

            gear_factors.extend(extract_neighbors(numbers_map[j], i, same_line=True))

            if j < max_y - 1:
                gear_factors.extend(extract_neighbors(numbers_map[j + 1], i))

            if len(gear_factors) == 2:
                gear_ratios.append(gear_factors[0] * gear_factors[1])

    # print(gear_ratios)
    return sum(gear_ratios)
