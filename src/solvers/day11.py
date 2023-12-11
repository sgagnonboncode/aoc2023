from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers
from math import lcm
from colorama import Fore, Back, Style

INPUT_FILE = "input/day11/part1.txt"
# INPUT_FILE = "input/day11/example.txt"


def parse_galaxies(lines: list[str]) -> list[list[int]]:
    galaxies: list[list[int]] = []

    for line in lines:
        galaxy_row = [i for i, ltr in enumerate(line) if ltr == "#"]
        row = [0] * len(line)
        for i in galaxy_row:
            row[i] = 1

        galaxies.append(row)

    return galaxies


def extract_galaxies_positions(galaxies_map: list[list[int]]) -> list[tuple[int, int]]:
    galaxies_pos = []
    for j in range(0, len(galaxies_map)):
        for i in range(0, len(galaxies_map[j])):
            if galaxies_map[j][i] == 1:
                galaxies_pos.append((i, j))

    return galaxies_pos


def compute_travel_cost_map(galaxies_map: list[list[int]], expansion_cost: int) -> int:
    travel_cost_map = [[1] * len(galaxies_map[0]) for _ in range(0, len(galaxies_map))]

    for j in range(0, len(galaxies_map)):
        row_cost = sum(galaxies_map[j])

        if row_cost == 0:
            travel_cost_map[j] = [expansion_cost] * len(galaxies_map[j])

    for i in range(0, len(galaxies_map[0])):
        col_cost = sum([galaxies_map[j][i] for j in range(0, len(galaxies_map))])

        if col_cost == 0:
            for j in range(0, len(galaxies_map)):
                travel_cost_map[j][i] = expansion_cost

    return travel_cost_map


def shortest_path(
    pos_a: tuple[int, int], pos_b: tuple[int, int], weight_map: list[list[int]]
) -> int:
    distance = 0
    orient_x = 1 if pos_b[0] > pos_a[0] else -1
    orient_y = 1 if pos_b[1] > pos_a[1] else -1

    current = pos_a

    max_x = len(weight_map[0])
    max_y = len(weight_map)

    while current != pos_b:
        x_move = (current[0] + orient_x, current[1])
        y_move = (current[0], current[1] + orient_y)

        # select best movement
        if x_move[0] < 0 or x_move[0] >= max_x or pos_b[0] - x_move[0] == -orient_x:
            current = y_move
        elif y_move[1] < 0 or y_move[1] >= max_y or pos_b[1] - y_move[1] == -orient_y:
            current = x_move
        elif weight_map[x_move[1]][x_move[0]] < weight_map[y_move[1]][y_move[0]]:
            current = x_move
        else:
            current = y_move

        distance += weight_map[current[1]][current[0]]

    return distance


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    galaxies_map = parse_galaxies(lines)

    galaxies_pos = extract_galaxies_positions(galaxies_map)
    travel_cost_map = compute_travel_cost_map(galaxies_map, 2)

    total_len = 0
    # sum pairs len
    for a in range(0, len(galaxies_pos) - 1):
        left = galaxies_pos[a]

        for b in range(a + 1, len(galaxies_pos)):
            right = galaxies_pos[b]

            distance = shortest_path(left, right, travel_cost_map)
            total_len += distance

    return total_len


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    galaxies_map = parse_galaxies(lines)

    galaxies_pos = extract_galaxies_positions(galaxies_map)
    travel_cost_map = compute_travel_cost_map(galaxies_map, 1000000)

    total_len = 0
    # sum pairs len
    for a in range(0, len(galaxies_pos) - 1):
        left = galaxies_pos[a]

        for b in range(a + 1, len(galaxies_pos)):
            right = galaxies_pos[b]

            distance = shortest_path(left, right, travel_cost_map)
            total_len += distance

    return total_len
