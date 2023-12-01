from common.file_helpers import read_lines


def scan_words(line) -> str:
    # insert numbers when words are found
    # for example: zoneight234 becomes z1on8eight234

    substitutions = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    processed = ""
    for i in range(0, len(line)):
        forward = line[i:]

        for word, number in substitutions.items():
            if forward.startswith(word):
                processed += number
                break

        processed += line[i]

    return processed


def filter_digits(line) -> int:
    "filter out non-digit characters"
    return "".join(filter(str.isdigit, line))


def extract_calibration_value(line) -> int:
    "extract calibration value from line"
    digits = filter_digits(line)
    return 10 * int(digits[0]) + int(digits[-1])


def solve_part1() -> int:
    lines = read_lines("input/day01/part1.txt")
    calibration_values = [extract_calibration_value(line) for line in lines]
    return sum(calibration_values)


def solve_part2() -> int:
    lines = read_lines("input/day01/part1.txt")
    word_replace = [scan_words(line) for line in lines]
    calibration_values = [extract_calibration_value(line) for line in word_replace]
    return sum(calibration_values)
