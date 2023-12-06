# import itertools
from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers

INPUT_FILE = "input/day06/part1.txt"
# INPUT_FILE = "input/day06/example.txt"


def solve_race_permutattions(duration: int, record: int) -> int:
    possible_speeds = 0

    for time_spent_boosting in range(0, duration):
        distance = (duration - time_spent_boosting) * time_spent_boosting
        if distance > record:
            possible_speeds+=1

    return possible_speeds


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    race_durations = extract_numbers(lines[0])
    race_record_distances = extract_numbers(lines[1])

    permutations = []
    for r in range(0, len(race_durations)):
        permutations.append(solve_race_permutattions(race_durations[r], race_record_distances[r]))

    score = 1
    for perm in permutations:
        score *= perm

    return score


def parse_line(line: str) -> int:
    accumulator = 0

    for d in [c for c in line if c.isdigit()]:
        accumulator *= 10
        accumulator += int(d)

    return accumulator


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    race_duration = parse_line(lines[0])
    record_distance = parse_line(lines[1])

    return solve_race_permutattions(race_duration, record_distance)
