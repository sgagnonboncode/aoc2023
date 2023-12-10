def extract_numbers(line: str) -> list[(int, int)]:
    number_map = []

    accumulator = 0
    entered = False
    for i in range(0, len(line)):
        char = line[i]

        # print(char, accumulator, entered, char.isdigit())

        if char.isdigit():
            entered = True
            accumulator *= 10
            accumulator += int(char)

        else:
            if entered:
                number_map.append(accumulator)
            entered = False
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


def extract_real_number(line: str) -> list[int]:
    return [int(n) for n in line.split()]
