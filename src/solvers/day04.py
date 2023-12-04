from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers


def find_loto_number_format(line: str) -> int:
    loto_nums = line.split("|")[0].split(":")[1]
    return len(loto_nums.strip().split(" "))


INPUT_FILE = "input/day04/part1.txt"
# INPUT_FILE = "input/day04/example.txt"


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    card_numbers_lines = [extract_numbers(line) for line in lines]
    loto_numbers = find_loto_number_format(lines[0])

    # print("Loto numbers:", loto_numbers)

    all_wins = []

    for card_numbers in card_numbers_lines:
        # play_number = card_numbers[0][1]
        winning_numbers = [n[1] for n in card_numbers[1 : loto_numbers + 1]]
        card_numbers = [n[1] for n in card_numbers[loto_numbers + 1 :]]

        nb_win = sum([1 for n in card_numbers if n in winning_numbers])
        score = pow(2, nb_win - 1) if nb_win > 0 else 0

        # print(play_number, winning_numbers, card_numbers, "Win:",nb_win, "Score:",score)
        all_wins.append(score)

    return sum(all_wins)


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    card_numbers_lines = [extract_numbers(line) for line in lines]
    loto_numbers = find_loto_number_format(lines[0])

    card_amount = [1 for line in lines]

    i = 0
    for card_numbers in card_numbers_lines:
        winning_numbers = [n[1] for n in card_numbers[1 : loto_numbers + 1]]
        card_numbers = [n[1] for n in card_numbers[loto_numbers + 1 :]]

        nb_win = sum([1 for n in card_numbers if n in winning_numbers])

        if nb_win > 0:
            for c in range(0, nb_win):
                card_amount[i + c + 1] += card_amount[i]

        i += 1

    # print(card_amount)
    return sum(card_amount)
