def extract_numbers(line: str) -> list[(int, int)]:
    number_map = []

    accumulator = 0
    for i in range(0, len(line)):
        char = line[i]

        if char.isdigit():
            accumulator *= 10
            accumulator += int(char)

        else:
            if accumulator > 0:
                number_map.append(accumulator)
            accumulator = 0
    if accumulator > 0:
        number_map.append(accumulator)

    return number_map


def extract_numbers_with_index(line: str) -> list[(int, int)]:
    number_map = []

    accumulator = 0
    number_index = 0
    for i in range(0, len(line)):
        char = line[i]

        if char.isdigit():
            if accumulator == 0:
                number_index = i
            accumulator *= 10
            accumulator += int(char)

        else:
            if accumulator > 0:
                number_map.append((number_index, accumulator))
            accumulator = 0
            number_index = 0
    if accumulator > 0:
        number_map.append((number_index, accumulator))

    return number_map
