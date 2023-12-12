from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers
from math import lcm
from colorama import Fore, Back, Style

INPUT_FILE = "input/day12/part1.txt"
# INPUT_FILE = "input/day12/example.txt"

solution_cache = {}


def solve_dynamic_programming(
    onsen: list[chr],
    control: list[int],
    onsen_pos: int,
    block_pos: int,
    current_block_len: int,
) -> int:
    cache_key = (onsen_pos, block_pos, current_block_len)

    # print(cache_key)

    if cache_key in solution_cache:
        # print("Cache hit ->",solution_cache[cache_key])
        return solution_cache[cache_key]

    if block_pos > len(control):
        # print("Block pos too high")
        return 0

    if onsen_pos >= len(onsen):
        if block_pos != len(control):
            # print("End of string : did not reach end of control")
            return 0

        # print("End of string : block match -> 1")
        return 1

    nb_permutations = 0

    if onsen[onsen_pos] in [".", "?"]:
        if current_block_len == 0:
            nb_permutations += solve_dynamic_programming(
                onsen, control, onsen_pos + 1, block_pos, 0
            )
        else:
            if block_pos >= len(control):
                pass
                # print("Block pos too high")
            elif control[block_pos] != current_block_len:
                pass
                # print("Block len not match", control[block_pos],'!=', current_block_len)
            else:
                nb_permutations += solve_dynamic_programming(
                    onsen, control, onsen_pos + 1, block_pos + 1, 0
                )

    if onsen[onsen_pos] in ["#", "?"]:
        if block_pos >= len(control):
            pass
            # print("Block pos too high")
        elif current_block_len < control[block_pos]:
            nb_permutations += solve_dynamic_programming(
                onsen, control, onsen_pos + 1, block_pos, current_block_len + 1
            )
        else:
            pass
            # print("Sequence too big")

    solution_cache[cache_key] = nb_permutations
    return nb_permutations


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    onsens = [line.split(" ")[0].strip() for line in lines]
    controls = []
    for line in lines:
        controls.append([int(n) for n in line.split(" ")[1].split(",")])

    score = 0
    for i in range(0, len(lines)):
        solution_cache.clear()
        local_score = solve_dynamic_programming(onsens[i] + ".", controls[i], 0, 0, 0)
        # print(onsens[i],controls[i]," -> ",local_score)
        score += local_score

    return score


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    onsens = [line.split(" ")[0].strip() for line in lines]
    controls = []
    for line in lines:
        controls.append([int(n) for n in line.split(" ")[1].split(",")])

    score = 0
    for i in range(0, len(lines)):
        solution_cache.clear()
        unfolded_onsen = (
            onsens[i]
            + "?"
            + onsens[i]
            + "?"
            + onsens[i]
            + "?"
            + onsens[i]
            + "?"
            + onsens[i]
        )
        unfolded_control = []
        for k in range(0, 5):
            for j in range(0, len(controls[i])):
                unfolded_control.append(controls[i][j])

        local_score = solve_dynamic_programming(
            unfolded_onsen + ".", unfolded_control, 0, 0, 0
        )
        # print(unfolded_onsen,unfolded_control," -> ",local_score)

        score += local_score

    return score
