def extract_grid_column(grid: list[str], i: int) -> str:
    column = ""

    for line in grid:
        column += line[i]

    return column
