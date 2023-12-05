# import itertools
from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers

INPUT_FILE = "input/day05/part1.txt"
# INPUT_FILE = "input/day05/example.txt"


class ConversionMap:
    def __init__(self, from_type: str, to_type: str):
        self.from_type = from_type
        self.to_type = to_type

        self.rules = []

    def add_range(self, source_min: int, destination_min: int, range_size: int):
        self.rules.append(
            {"source": source_min, "destination": destination_min, "size": range_size}
        )

    def convert(self, source: int) -> int:
        for rule in self.rules:
            min_source = rule["source"]
            max_source = rule["source"] + rule["size"] - 1

            if source < min_source or source > max_source:
                continue

            return rule["destination"] + (source - min_source)

        return source


def evaluate_seed(almanac: dict[str, ConversionMap], seed: int) -> int:
    current_type = "seed"
    current_index = seed

    while current_type != "location":
        next_index = almanac[current_type].convert(current_index)
        next_type = almanac[current_type].to_type

        # print("From",current_type,current_index,"To",next_type, next_index)

        current_index = next_index
        current_type = next_type

    return current_index


def parse_almanac(lines: list[str]) -> dict[str, ConversionMap]:
    # skip two lines

    maps = {}

    active_type: str = None
    for line in lines[1:]:
        if len(line) == 0:
            active_type = None
        else:
            if active_type is None:
                conv_type = line.split(" ")[0].split("-")

                from_type = conv_type[0]
                to_type = conv_type[-1]
                active_type = from_type

                maps[active_type] = ConversionMap(from_type, to_type)
            else:
                numbers = extract_numbers(line)
                maps[active_type].add_range(numbers[1], numbers[0], numbers[2])

    return maps


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    seeds = extract_numbers(lines[0])
    almanac = parse_almanac(lines)

    seed_locations = [evaluate_seed(almanac, seed) for seed in seeds]
    return min(seed_locations)


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    seeds_nums = extract_numbers(lines[0])
    almanac = parse_almanac(lines)

    # create a list of ranges to evaluate and affine it for every discontinuity discovered
    seed_ranges = []

    # initial input
    for i in range(0, len(seeds_nums), 2):
        seed_start = seeds_nums[i]
        seed_range = seeds_nums[i + 1]

        seed_ranges.append((seed_start, seed_start + seed_range))

    # iterate over the rules and look for discontinuities

    has_discontinuity = True
    while has_discontinuity:
        seed_ranges.sort(key=lambda x: x[0])

        has_discontinuity = False

        for i in range(0, len(seed_ranges)):
            if has_discontinuity:
                break

            seed_range = seed_ranges[i]
            seed_start = seed_range[0]
            seed_end = seed_range[1]

            max_dist = seed_end - seed_start

            # print("Checking range",seed_range,"with max dist",max_dist)

            current_type = "seed"

            current_value = seed_start

            while current_type != "location":
                if has_discontinuity:
                    break

                next_value = almanac[current_type].convert(current_value)
                next_type = almanac[current_type].to_type

                for rule in almanac[current_type].rules:
                    min_source = rule["source"]
                    max_source = rule["source"] + rule["size"] - 1

                    if current_value < min_source or current_value > max_source:
                        continue

                    rule_dist = max_source - current_value
                    if rule_dist < max_dist:
                        # print("Discontinuity found in type",current_type)
                        # print("Max dist",max_dist,"Rule dist",rule_dist)
                        has_discontinuity = True

                        seed_ranges[i] = (seed_start, seed_start + rule_dist)
                        seed_ranges.append((seed_start + rule_dist + 1, seed_end))

                        break

                current_type = next_type
                current_value = next_value

    local_min_locations = []
    for seed_range in seed_ranges:
        # evaluate the first value of the continuous range since it's the minimum by definition
        local_min_locations.append(evaluate_seed(almanac, seed_range[0]))

    return min(local_min_locations)
