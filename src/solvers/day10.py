from common.file_helpers import read_lines
from common.extract_numbers import extract_numbers
from math import lcm
from colorama import Fore, Back, Style

INPUT_FILE = "input/day10/part1.txt"
# INPUT_FILE = "input/day10/example.txt"
# INPUT_FILE = "input/day10/example_3.txt"


def follow_path(
    lines: list[str], start_pos: tuple[str, str], previous: tuple[str, str]
) -> tuple[str, str]:
    x_start, y_start = start_pos
    x_prev, y_prev = previous

    current = lines[y_start][x_start]

    # test left
    if (
        current not in ["|", "L", "F"]
        and x_start > 0
        and x_prev != x_start - 1
        and lines[y_start][x_start - 1] in ("-", "F", "L")
    ):
        return (x_start - 1, y_start)

    # test right
    if (
        current not in ["|", "J", "7"]
        and x_start < len(lines[y_start]) - 1
        and x_prev != x_start + 1
        and lines[y_start][x_start + 1] in ("-", "J", "7")
    ):
        return (x_start + 1, y_start)

    # test up
    if (
        current not in ["-", "7", "F"]
        and y_start > 0
        and y_prev != y_start - 1
        and lines[y_start - 1][x_start] in ("|", "F", "7")
    ):
        return (x_start, y_start - 1)

    # test down
    if (
        current not in ["-", "L", "J"]
        and y_start < len(lines) - 1
        and y_prev != y_start + 1
        and lines[y_start + 1][x_start] in ("|", "J", "L")
    ):
        return (x_start, y_start + 1)

    raise ValueError("No path found")


def solve_part1() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]

    x_start = 0
    y_start = 0
    for i in range(0, len(lines)):
        x_start = lines[i].find("S")
        if x_start != -1:
            y_start = i
            break

    # print("X:", x_start, "Y:", y_start)

    forward_pos = (x_start, y_start)
    previous_forward_pos = (x_start, y_start)

    backward_pos = (x_start, y_start)
    previous_backward_pos = (x_start, y_start)

    steps = 0

    assigned = 0

    # on the first step decide which direction to go
    # test left
    if x_start > 0 and lines[y_start][x_start - 1] in ("-", "F", "L"):
        backward_pos = (x_start - 1, y_start)
        assigned += 1

    # test right
    if x_start < len(lines[y_start]) - 1 and lines[y_start][x_start + 1] in (
        "-",
        "J",
        "7",
    ):
        if assigned == 0:
            backward_pos = (x_start + 1, y_start)
        else:
            forward_pos = (x_start + 1, y_start)
        assigned += 1

    # test up
    if y_start > 0 and lines[y_start - 1][x_start] in ("|", "F", "7"):
        if assigned == 0:
            backward_pos = (x_start, y_start - 1)
        else:
            forward_pos = (x_start, y_start - 1)
        assigned += 1

    # test down
    if y_start < len(lines) - 1 and lines[y_start + 1][x_start] in ("|", "J", "L"):
        if assigned == 0:
            backward_pos = (x_start, y_start + 1)
        else:
            forward_pos = (x_start, y_start + 1)
        assigned += 1

    # print("Assigned:", assigned)
    # print("Forward:", forward_pos)
    # print("Backward:", backward_pos)
    steps += 1

    while True:
        next_forward = follow_path(lines, forward_pos, previous_forward_pos)
        next_backward = follow_path(lines, backward_pos, previous_backward_pos)

        if next_forward == next_backward:
            steps += 1
            break

        elif next_forward == previous_backward_pos:
            break

        steps += 1
        previous_forward_pos = forward_pos
        forward_pos = next_forward

        previous_backward_pos = backward_pos
        backward_pos = next_backward

    #     print("Step ", steps, ":", forward_pos, backward_pos)

    # print(steps)

    return steps


GRADIENT_TOP_LEFT = "↖"
GRADIENT_LEFT = "←"
GRADIENT_BOTTOM_LEFT = "↙"
GRADIENT_TOP = "↑"
GRADIENT_BOTTOM = "↓"
GRADIENT_TOP_RIGHT = "↗"
GRADIENT_RIGHT = "→"
GRADIENT_BOTTOM_RIGHT = "↘"


def solve_part2() -> int:
    lines = [line.strip() for line in read_lines(INPUT_FILE)]
    visited = []
    gradient = []
    for i in range(0, len(lines)):
        visited.append([])
        gradient.append([])
        for j in range(0, len(lines[i])):
            gradient[i].append(" ")

            # the sides may never be fully envelopped
            if i == 0 or j == 0 or i == len(lines) - 1 or j == len(lines[i]) - 1:
                visited[i].append(" ")
            else:
                visited[i].append("?")

    x_start = 0
    y_start = 0
    for i in range(0, len(lines)):
        x_start = lines[i].find("S")
        if x_start != -1:
            y_start = i
            break

    forward_pos = (x_start, y_start)
    previous_forward_pos = (x_start, y_start)

    assigned = 0

    forward_pos = (x_start, y_start)
    previous_forward_pos = (x_start, y_start)
    backward_pos = (x_start, y_start)

    assigned = 0

    # on the first step decide which direction to go
    # test left
    if x_start > 0 and lines[y_start][x_start - 1] in ("-", "F", "L"):
        backward_pos = (x_start - 1, y_start)
        assigned += 1

    # test right
    if x_start < len(lines[y_start]) - 1 and lines[y_start][x_start + 1] in (
        "-",
        "J",
        "7",
    ):
        if assigned == 0:
            backward_pos = (x_start + 1, y_start)
        else:
            forward_pos = (x_start + 1, y_start)
        assigned += 1

    # test up
    if y_start > 0 and lines[y_start - 1][x_start] in ("|", "F", "7"):
        if assigned == 0:
            backward_pos = (x_start, y_start - 1)
        else:
            forward_pos = (x_start, y_start - 1)
        assigned += 1

    # test down
    if y_start < len(lines) - 1 and lines[y_start + 1][x_start] in ("|", "J", "L"):
        if assigned == 0:
            backward_pos = (x_start, y_start + 1)
        else:
            forward_pos = (x_start, y_start + 1)
        assigned += 1

    visited[y_start][x_start] = "V"
    visited[forward_pos[1]][forward_pos[0]] = "V"
    visited[backward_pos[1]][backward_pos[0]] = "V"

    while True:
        next_forward = follow_path(lines, forward_pos, previous_forward_pos)

        delta_x = next_forward[0] - forward_pos[0]
        delta_y = next_forward[1] - forward_pos[1]

        current = lines[forward_pos[1]][forward_pos[0]]

        if current == "F" and delta_x == 1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_BOTTOM_RIGHT
        elif current == "F" and delta_y == 1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_TOP_LEFT
        elif current == "7" and delta_x == -1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_TOP_RIGHT
        elif current == "7" and delta_y == 1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_BOTTOM_LEFT
        elif current == "J" and delta_x == -1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_TOP_LEFT
        elif current == "J" and delta_y == -1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_BOTTOM_RIGHT
        elif current == "L" and delta_x == 1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_BOTTOM_LEFT
        elif current == "L" and delta_y == -1:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_TOP_RIGHT
        elif current == "|" and gradient[previous_forward_pos[1]][
            previous_forward_pos[0]
        ] in [GRADIENT_TOP_RIGHT, GRADIENT_RIGHT, GRADIENT_BOTTOM_RIGHT]:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_RIGHT
        elif current == "|" and gradient[previous_forward_pos[1]][
            previous_forward_pos[0]
        ] in [GRADIENT_BOTTOM_LEFT, GRADIENT_LEFT, GRADIENT_TOP_LEFT]:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_LEFT
        elif current == "-" and gradient[previous_forward_pos[1]][
            previous_forward_pos[0]
        ] in [GRADIENT_BOTTOM_LEFT, GRADIENT_BOTTOM, GRADIENT_BOTTOM_RIGHT]:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_BOTTOM
        elif current == "-" and gradient[previous_forward_pos[1]][
            previous_forward_pos[0]
        ] in [GRADIENT_TOP_LEFT, GRADIENT_TOP, GRADIENT_TOP_RIGHT]:
            gradient[forward_pos[1]][forward_pos[0]] = GRADIENT_TOP

        if next_forward == backward_pos:
            break

        previous_forward_pos = forward_pos
        forward_pos = next_forward

        visited[forward_pos[1]][forward_pos[0]] = "V"

    # reduce until we cannot reduce
    reduced = True
    while reduced:
        reduced = False

        for j in range(0, len(visited)):
            for i in range(0, len(visited[j])):
                # expand impossible zone

                # down
                if (
                    j < len(visited) - 1
                    and visited[j][i] == "?"
                    and visited[j + 1][i] == " "
                ):
                    visited[j][i] = " "
                    reduced = True

                # up
                if j > 0 and visited[j][i] == "?" and visited[j - 1][i] == " ":
                    visited[j][i] = " "
                    reduced = True

                # left
                if i > 0 and visited[j][i] == "?" and visited[j][i - 1] == " ":
                    visited[j][i] = " "
                    reduced = True

                # right
                if (
                    i < len(visited[j]) - 1
                    and visited[j][i] == "?"
                    and visited[j][i + 1] == " "
                ):
                    visited[j][i] = " "
                    reduced = True

                # special exception : diagonals adjacent to impossible envelopment spread
                if (
                    i > 0
                    and j > 0
                    and visited[j - 1][i - 1] == " "
                    and visited[j][i] == "?"
                ):
                    visited[j][i] = " "
                    reduced = True

                if (
                    i < len(visited[j]) - 1
                    and j > 0
                    and visited[j - 1][i + 1] == " "
                    and visited[j][i] == "?"
                ):
                    visited[j][i] = " "
                    reduced = True
                if (
                    i > 0
                    and j < len(visited) - 1
                    and visited[j + 1][i - 1] == " "
                    and visited[j][i] == "?"
                ):
                    visited[j][i] = " "
                    reduced = True
                if (
                    i < len(visited[j]) - 1
                    and j < len(visited) - 1
                    and visited[j + 1][i + 1] == " "
                    and visited[j][i] == "?"
                ):
                    visited[j][i] = " "
                    reduced = True

    # affect gradient to still unknown
    for j in range(0, len(visited)):
        for i in range(0, len(visited[j])):
            if visited[j][i] != "?":
                continue

            # test all 8 directions
            # top left
            if i > 0 and j > 0 and gradient[j - 1][i - 1] == GRADIENT_BOTTOM_RIGHT:
                visited[j][i] = "I"
                continue

            # top
            if j > 0 and gradient[j - 1][i] in [
                GRADIENT_BOTTOM,
                GRADIENT_BOTTOM_LEFT,
                GRADIENT_BOTTOM_RIGHT,
            ]:
                visited[j][i] = "I"
                continue

            # top right
            if (
                i < len(visited[j]) - 1
                and j > 0
                and gradient[j - 1][i + 1] == GRADIENT_BOTTOM_LEFT
            ):
                visited[j][i] = "I"
                continue

            # left
            if i > 0 and gradient[j][i - 1] in [
                GRADIENT_RIGHT,
                GRADIENT_TOP_RIGHT,
                GRADIENT_BOTTOM_RIGHT,
            ]:
                visited[j][i] = "I"
                continue

            # right
            if i < len(visited[j]) - 1 and gradient[j][i + 1] in [
                GRADIENT_LEFT,
                GRADIENT_TOP_LEFT,
                GRADIENT_BOTTOM_LEFT,
            ]:
                visited[j][i] = "I"
                continue

            # bottom left
            if (
                i > 0
                and j < len(visited) - 1
                and gradient[j + 1][i - 1] == GRADIENT_TOP_RIGHT
            ):
                visited[j][i] = "I"
                continue

            # bottom
            if j < len(visited) - 1 and gradient[j + 1][i] in [
                GRADIENT_TOP,
                GRADIENT_TOP_LEFT,
                GRADIENT_TOP_RIGHT,
            ]:
                visited[j][i] = "I"
                continue

            # bottom right
            if (
                i < len(visited[j]) - 1
                and j < len(visited) - 1
                and gradient[j + 1][i + 1] == GRADIENT_TOP_LEFT
            ):
                visited[j][i] = "I"
                continue

    # final pass : grow 'I'
    grow = True
    while grow:
        grow = False
        for j in range(0, len(visited)):
            for i in range(0, len(visited[j])):
                if visited[j][i] != "?":
                    continue

                # grow left
                if i > 0 and visited[j][i - 1] == "I":
                    visited[j][i] = "I"
                    grow = True
                    continue

                # grow right
                if i < len(visited[j]) - 1 and visited[j][i + 1] == "I":
                    visited[j][i] = "I"
                    grow = True
                    continue

                # grow up
                if j > 0 and visited[j - 1][i] == "I":
                    visited[j][i] = "I"
                    grow = True
                    continue

                # grow down
                if j < len(visited) - 1 and visited[j + 1][i] == "I":
                    visited[j][i] = "I"
                    grow = True
                    continue

    score = 0
    for j in range(0, len(visited)):
        for i in range(0, len(visited[j])):
            # if visited[j][i] != "V":
            #     print(Fore.WHITE, visited[j][i], end="")
            # elif gradient[j][i] == " ":
            #     print(Fore.RED, lines[j][i], end="")
            # else:
            #     print(Fore.GREEN, gradient[j][i], end="")

            if visited[j][i] == "I":
                score += 1
        # print()

    return score
