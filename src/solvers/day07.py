# import itertools
import math
from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers
from functools import cmp_to_key

INPUT_FILE = "input/day07/part1.txt"
# INPUT_FILE = "input/day07/example.txt"


def count_figures(hand: str) -> dict[str, int]:
    figures = {}

    for card in hand:
        if card not in figures:
            figures[card] = 0
        figures[card] += 1

    return figures


def filter_jokers(figures: dict[dict[str, int]]) -> dict[dict[str, int]]:
    return {k: v for k, v in figures.items() if k != "J"}


# hand strengh analysis is done with the presumption that stronger hands are already tested for
def is_five_of_a_kind(figures: dict[str, int], joker_rules: bool = False) -> bool:
    if len(figures) == 1:
        return True

    if figures.get("J", 0) > 0 and joker_rules:
        return len(figures) == 2

    return False


def is_four_of_a_kind(figures: dict[str, int], joker_rules: bool = False) -> bool:
    if len(figures) == 2 and max(figures.values()) == 4:
        return True

    if figures.get("J", 0) > 0 and joker_rules:
        return max([v for v in filter_jokers(figures).values()]) + figures["J"] == 4

    return False


def is_full_house(figures: dict[str, int], joker_rules: bool = False) -> bool:
    if len(figures) == 2 and max(figures.values()) == 3:
        return True

    if figures.get("J", 0) > 0 and joker_rules:
        return len([v for v in filter_jokers(figures).values()]) == 2

    return False


def is_three_of_a_kind(figures: dict[str, int], joker_rules: bool = False) -> bool:
    if len(figures) == 3 and max(figures.values()) == 3:
        return True

    if figures.get("J", 0) > 0 and joker_rules:
        return max([v for v in filter_jokers(figures).values()]) + figures["J"] == 3

    return False


def is_two_pairs(figures: dict[str, int], joker_rules: bool = False) -> bool:
    if len(figures) == 3 and max(figures.values()) == 2:
        return True

    if figures.get("J", 0) > 0 and joker_rules:
        if figures["J"] == 2:
            return True

        return max([v for v in filter_jokers(figures).values()]) == 2

    return False


def is_one_pair(figures: dict[str, int], joker_rules: bool = False) -> bool:
    if len(figures) == 4 and max(figures.values()) == 2:
        return True

    if figures.get("J", 0) > 0 and joker_rules:
        # automatically true if there is a joker
        return True

    return False


HAND_STRENGTH = [
    "FiveOfAKind",
    "FourOfAKind",
    "FullHouse",
    "ThreeOfAKind",
    "TwoPairs",
    "OnePair",
    "HighCard",
]


def assign_hand_strength(hand: str, joker_rules: bool = False) -> str:
    figures = count_figures(hand)

    if is_five_of_a_kind(figures, joker_rules):
        return "FiveOfAKind"
    elif is_four_of_a_kind(figures, joker_rules):
        return "FourOfAKind"
    elif is_full_house(figures, joker_rules):
        return "FullHouse"
    elif is_three_of_a_kind(figures, joker_rules):
        return "ThreeOfAKind"
    elif is_two_pairs(figures, joker_rules):
        return "TwoPairs"
    elif is_one_pair(figures, joker_rules):
        return "OnePair"
    else:
        return "HighCard"


SUITS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
JOKER_RULES_SUITS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def break_equality(hand1: str, hand2: str, joker_rules: bool = False) -> int:
    comparison_ranking = JOKER_RULES_SUITS if joker_rules else SUITS

    for i in range(0, len(hand1)):
        if hand1[i] == hand2[i]:
            continue
        else:
            return (
                -1
                if comparison_ranking.index(hand1[i])
                < comparison_ranking.index(hand2[i])
                else 1
            )


def sort_compare(
    left: (str, int, str), right: (str, int, str), joker_rules: bool = False
) -> int:
    if HAND_STRENGTH.index(left[2]) != HAND_STRENGTH.index(right[2]):
        return -1 if HAND_STRENGTH.index(left[2]) < HAND_STRENGTH.index(right[2]) else 1

    return break_equality(left[0], right[0], joker_rules)


def sort_hands(
    hands: list[(str, int, str)], joker_rules: bool = False
) -> list[(str, int, str)]:
    sorted = False
    while not sorted:
        sorted = True
        for i in range(0, len(hands) - 1):
            if sort_compare(hands[i], hands[i + 1], joker_rules) < 0:
                sorted = False
                hands[i], hands[i + 1] = hands[i + 1], hands[i]

    return hands


def solve(joker_rules: bool) -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    left_right = [line.split(" ") for line in lines]
    hands = [
        (lr[0], int(lr[1]), assign_hand_strength(lr[0], joker_rules))
        for lr in left_right
    ]

    hands = sort_hands(hands, joker_rules)

    score = 0
    for i in range(0, len(hands)):
        # if(joker_rules):
        #     print(hands[i][0], hands[i][2].ljust(15,' ') , len([c for c in hands[i][0] if c == "J"]), count_figures(hands[i][0]))

        hand_score = hands[i][1] * (i + 1)
        score += hand_score

    return score


def solve_part1() -> int:
    return solve(joker_rules=False)


def solve_part2() -> int:
    return solve(joker_rules=True)
