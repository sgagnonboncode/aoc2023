from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers, extract_real_numbers
from math import lcm
from colorama import Fore, Back, Style

INPUT_FILE = "input/day16/part1.txt"
# INPUT_FILE = "input/day16/example.txt"


def parse_map(lines: list[str]) -> list[list[str]]:
    map = []
    for line in lines:
        map.append([c for c in line])
    return map


def beam_logic(
    map: list[list[str]], x: int, y: int, orient_x: int, orient_y: int
) -> list((int, int, int, int)):
    nx = x + orient_x
    ny = y + orient_y

    if (orient_x != 0 and orient_y != 0) or (orient_x == 0 and orient_y == 0):
        raise ValueError("Invalid beam orientation")

    next_beams: list[(int, int, int, int)] = []

    if nx >= 0 and nx < len(map[0]) and ny >= 0 and ny < len(map):
        if map[ny][nx] == ".":
            next_beams.append((nx, ny, orient_x, orient_y))

        elif map[ny][nx] in ["|", "-"]:
            if orient_x != 0 and map[ny][nx] == "-":
                # keep going
                next_beams.append((nx, ny, orient_x, orient_y))
            elif orient_y != 0 and map[ny][nx] == "|":
                # keep going
                next_beams.append((nx, ny, orient_x, orient_y))

            elif orient_x != 0 and map[ny][nx] == "|":
                # split
                next_beams.append((nx, ny, 0, 1))
                next_beams.append((nx, ny, 0, -1))
            elif orient_y != 0 and map[ny][nx] == "-":
                # split
                next_beams.append((nx, ny, 1, 0))
                next_beams.append((nx, ny, -1, 0))

        elif map[ny][nx] in ["\\", "/"]:
            if orient_x != 0 and map[ny][nx] == "\\":
                next_beams.append((nx, ny, 0, orient_x))
            elif orient_y != 0 and map[ny][nx] == "\\":
                next_beams.append((nx, ny, orient_y, 0))
            elif orient_x != 0 and map[ny][nx] == "/":
                next_beams.append((nx, ny, 0, -orient_x))
            elif orient_y != 0 and map[ny][nx] == "/":
                next_beams.append((nx, ny, -orient_y, 0))

    return next_beams


def compute_beam_energizing_count(
    map: list[list[str]], starting_position: (int, int, int, int)
) -> int:
    energized_map = [[0] * len(map[0]) for _ in range(0, len(map))]
    beams = [starting_position]
    seen_positions: set[(int, int, int, int)] = set()
    while len(beams) > 0:
        next_beams = []
        for beam in beams:
            next_beams.extend(beam_logic(map, beam[0], beam[1], beam[2], beam[3]))

            if beam != starting_position:
                energized_map[beam[1]][beam[0]] = 1

        beams = []
        for beam in next_beams:
            if beam in seen_positions:
                # print("Already seen",beam)
                pass
            else:
                seen_positions.add(beam)
                beams.append(beam)

    return sum([sum(line) for line in energized_map])


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    map = parse_map(lines)

    return compute_beam_energizing_count(map, (-1, 0, 1, 0))


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    map = parse_map(lines)

    starting_positions: list[(int, int, int, int)] = []

    for y in range(0, len(map)):
        # left and right borders
        starting_positions.append((-1, y, 1, 0))
        starting_positions.append((len(map[0]), y, -1, 0))

    for x in range(0, len(map[0])):
        # top and bottom borders
        starting_positions.append((x, -1, 0, 1))
        starting_positions.append((x, len(map), 0, -1))

    best_score: int = 0

    for starting_position in starting_positions:
        score = compute_beam_energizing_count(map, starting_position)

        if score > best_score:
            best_score = score

    return best_score
