from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers
from math import lcm
from colorama import Fore, Back, Style

INPUT_FILE = "input/day13/part1.txt"
# INPUT_FILE = "input/day13/example.txt"


def parse_grids(lines: list[str]) -> list[list[str]]:
    grids = []

    accumulator = []

    for line in lines:
        if len(line) == 0:
            grids.append(accumulator)
            accumulator = []
            continue

        accumulator.append(line)

    grids.append(accumulator)
    return grids


def smudge_fixable(left: str, right: str) -> bool:
    nb_smudges = 0

    for i in range(0, len(left)):
        if left[i] != right[i] and (left[i] == "." or right[i] == "."):
            nb_smudges += 1

    return nb_smudges == 1


def find_horizontal_reflection(grid: list[str], smudge_logic=False) -> int:
    grid_size = len(grid)

    for mid_row in range(grid_size - 2, -1, -1):
        local_row_match = 0

        mismatch = False
        smudge_fixed = False

        while mid_row - local_row_match >= 0:
            if mid_row + local_row_match + 1 >= grid_size:
                break

            row_left = grid[mid_row - local_row_match]
            row_right = grid[mid_row + local_row_match + 1]

            if row_left == row_right:
                local_row_match += 1
            else:
                if smudge_logic and not smudge_fixed:
                    if smudge_fixable(row_left, row_right):
                        smudge_fixed = True
                        local_row_match += 1
                    else:
                        local_row_match = 0
                        mismatch = True
                        break
                else:
                    local_row_match = 0
                    mismatch = True
                    break

        if mismatch or (smudge_logic and not smudge_fixed):
            continue

        return mid_row

    # special case for duplicate on first row
    if smudge_logic and smudge_fixable(grid[0], grid[1]):
        return 0
    elif not smudge_logic and grid[0] == grid[1]:
        return 0

    return -1


def extract_grid_column(grid: list[str], i: int) -> str:
    column = ""

    for line in grid:
        column += line[i]

    return column


def find_vertical_reflection(grid: list[str], smudge_logic=False) -> int:
    grid_size = len(grid[0])

    for mid_row in range(grid_size - 2, -1, -1):
        local_row_match = 0

        mismatch = False
        smudge_fixed = False
        while mid_row - local_row_match >= 0:
            if mid_row + local_row_match + 1 >= grid_size:
                break

            col_left = extract_grid_column(grid, mid_row - local_row_match)
            col_right = extract_grid_column(grid, mid_row + local_row_match + 1)

            if col_left == col_right:
                local_row_match += 1
            else:
                if smudge_logic and not smudge_fixed:
                    if smudge_fixable(col_left, col_right):
                        smudge_fixed = True
                        local_row_match += 1
                    else:
                        local_row_match = 0
                        mismatch = True
                        break
                else:
                    local_row_match = 0
                    mismatch = True
                    break

        if mismatch or (smudge_logic and not smudge_fixed):
            continue

        return mid_row

    # special case for duplicate on first column
    col_0 = extract_grid_column(grid, 0)
    col_1 = extract_grid_column(grid, 1)

    if smudge_logic and smudge_fixable(col_0, col_1):
        return 0
    elif not smudge_logic and col_0 == grid[1]:
        return 0

    return -1


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    grids = parse_grids(lines)

    score = 0
    for i in range(0, len(grids)):
        # print("Grid", i)

        # for line in grids[i]:
        #     print(line)

        row_reflection = find_horizontal_reflection(grids[i])
        col_reflection = find_vertical_reflection(grids[i])

        if row_reflection < 0 and col_reflection < 0:
            # print("No Reflection on grid", i)
            raise ValueError("No Reflection")
        elif col_reflection < 0:
            # print("Row Reflection at", row_reflection+1)
            score += 100 * (row_reflection + 1)
        elif row_reflection < 0:
            # print("Col Reflection at", col_reflection+1)
            score += col_reflection + 1
        else:
            # print("Ambiguous reflection on grid", i)
            # print("Row Reflection at", row_reflection+1)
            # print("Col Reflection at", col_reflection+1)
            raise ValueError("No Reflection")

    return score


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    grids = parse_grids(lines)

    score = 0
    for i in range(0, len(grids)):
        # print("Grid", i)

        # for line in grids[i]:
        #     print(line)

        row_reflection = find_horizontal_reflection(grids[i], smudge_logic=True)
        col_reflection = find_vertical_reflection(grids[i], smudge_logic=True)

        if row_reflection < 0 and col_reflection < 0:
            # print("No Reflection on grid", i)
            raise ValueError("No Reflection")
        elif col_reflection < 0:
            # print("Row Reflection at", row_reflection+1)
            score += 100 * (row_reflection + 1)
        elif row_reflection < 0:
            # print("Col Reflection at", col_reflection+1)
            score += col_reflection + 1
        else:
            # print("Ambiguous reflection on grid", i)
            # print("Row Reflection at", row_reflection+1)
            # print("Col Reflection at", col_reflection+1)
            raise ValueError("No Reflection")

    return score
