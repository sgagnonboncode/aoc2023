from common.file_helpers import read_lines


def parse_line(line) -> tuple[int, list[int, int, int]]:
    game_sep = line.split(":")
    game_id = int(game_sep[0].split(" ")[1])
    records = game_sep[1].split(";")
    details = []

    for record in records:
        red = 0
        green = 0
        blue = 0
        tokens = [r.strip() for r in record.split(",")]

        for token in tokens:
            split = token.split(" ")

            if split[1] == "red":
                red += int(split[0])
            elif split[1] == "green":
                green += int(split[0])
            elif split[1] == "blue":
                blue += int(split[0])

        details.append([red, green, blue])

    return game_id, details


def solve_part1() -> int:
    lines = read_lines("input/day02/part1.txt")
    # lines = read_lines("input/day02/example.txt")
    games = [parse_line(line) for line in lines]

    criteria_red = 12
    criteria_green = 13
    criteria_blue = 14

    score = 0

    for game in games:
        red = max([d[0] for d in game[1]])
        green = max([d[1] for d in game[1]])
        blue = max([d[2] for d in game[1]])

        if red <= criteria_red and green <= criteria_green and blue <= criteria_blue:
            # print(game[0],"R",red,"G", green,"B", blue, "is possible")
            score += game[0]

    return score


def solve_part2() -> int:
    lines = read_lines("input/day02/part1.txt")
    # lines = read_lines("input/day02/example.txt")
    games = [parse_line(line) for line in lines]

    score = 0

    for game in games:
        red = max([d[0] for d in game[1]])
        green = max([d[1] for d in game[1]])
        blue = max([d[2] for d in game[1]])

        power = red * green * blue
        # print("Game",game[0],"R",red,"G", green,"B", blue, "power",power)
        score += power

    return score
