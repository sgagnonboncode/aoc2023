from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers, extract_real_numbers
from math import lcm
from colorama import Fore, Back, Style

INPUT_FILE = "input/day14/part1.txt"
# INPUT_FILE = "input/day14/example.txt"


def parse_grid(lines: list[str]) -> list[list[str]]:
    grid = []

    for line in lines:
        grid.append([c for c in line])

    return grid


def tilt_north(grid: list[list[str]]) -> list[list[str]]:
    for j in range(1, len(grid)):
        for i in range(0, len(grid[j])):
            if grid[j][i] != "O":
                continue

            # find the topmost north spot to roll the rock on
            can_roll = False
            k = j
            while k > 0:
                if grid[k - 1][i] != ".":
                    break

                can_roll = True
                k -= 1

            if can_roll:
                # print("Rolling rock from",j,i,"to",k,i)
                grid[k][i] = "O"
                grid[j][i] = "."

    return grid


def tilt_south(grid: list[list[str]]) -> list[list[str]]:
    for j in range(len(grid) - 2, -1, -1):
        for i in range(0, len(grid[j])):
            if grid[j][i] != "O":
                continue

            # find the bottom most spot to roll the rock on
            can_roll = False
            k = j
            while k < len(grid) - 1:
                if grid[k + 1][i] != ".":
                    break

                can_roll = True
                k += 1

            if can_roll:
                # print("Rolling rock from",j,i,"to",k,i)
                grid[k][i] = "O"
                grid[j][i] = "."

    return grid


def tilt_west(grid: list[list[str]]) -> list[list[str]]:
    for i in range(1, len(grid[0])):
        for j in range(0, len(grid)):
            if grid[j][i] != "O":
                continue

            # find the leftmost spot to roll the rock on
            can_roll = False
            k = i
            while k > 0:
                if grid[j][k - 1] != ".":
                    break

                can_roll = True
                k -= 1

            if can_roll:
                # print("Rolling rock from",j,i,"to",j,k)
                grid[j][k] = "O"
                grid[j][i] = "."

    return grid


def tilt_east(grid: list[list[str]]) -> list[list[str]]:
    for i in range(len(grid[0]) - 2, -1, -1):
        for j in range(0, len(grid)):
            if grid[j][i] != "O":
                continue

            # find the leftmost spot to roll the rock on
            can_roll = False
            k = i
            while k < len(grid[0]) - 1:
                if grid[j][k + 1] != ".":
                    break

                can_roll = True
                k += 1

            if can_roll:
                # print("Rolling rock from",j,i,"to",j,k)
                grid[j][k] = "O"
                grid[j][i] = "."

    return grid


def compute_north_load(grid: list[list[str]]) -> int:
    north_load = 0
    nb_rows = len(grid)
    cur_row = 0
    for row in grid:
        north_load += sum([1 for c in row if c == "O"]) * (nb_rows - cur_row)
        cur_row += 1

    return north_load


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    grid = parse_grid(lines)
    grid = tilt_north(grid)
    return compute_north_load(grid)


def compare_grids(grid1: list[list[str]], grid2: list[list[str]]) -> bool:
    for j in range(0, len(grid1)):
        for i in range(0, len(grid1[j])):
            if grid1[j][i] != grid2[j][i]:
                return False

    return True


def analyse_load_pattern(load_pattern: list[int], test_iterations: int = 20) -> int:
    sequence_length = 1
    while sequence_length < len(load_pattern):
        sequence = load_pattern[-sequence_length:]

        # print("Sequence length", sequence_length , " : ", sequence)

        pattern_found = True
        # test pattern
        for k in range(0, test_iterations):
            for l in range(0, sequence_length):
                if load_pattern[-(k + 1) * sequence_length + l] != sequence[l]:
                    # print("No match at", k*sequence_length+l, ":", (k+1)*sequence_length+l)
                    # print(load_pattern[-(k+1)*sequence_length:-(k)*sequence_length])
                    pattern_found = False
                    break

        if pattern_found:
            return sequence_length

        sequence_length += 1

    raise ValueError("No pattern found in sample")


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    grid = parse_grid(lines)

    load_pattern = []
    total_cycles = 1000000000
    sample_cycles = 500

    # take a sample of cycles in order to analyse for a pattern
    for i in range(0, sample_cycles):
        grid = tilt_north(grid)
        grid = tilt_west(grid)
        grid = tilt_south(grid)
        grid = tilt_east(grid)

        load_pattern.append(compute_north_load(grid))

    sequence_length = analyse_load_pattern(load_pattern)
    # print("Sequence length", sequence_length , " : ", load_pattern[-sequence_length:])

    # extrapolate cycles
    remaining_cycles = total_cycles - sample_cycles - 1
    sequence_pos = remaining_cycles % sequence_length
    return load_pattern[-sequence_length + sequence_pos]
