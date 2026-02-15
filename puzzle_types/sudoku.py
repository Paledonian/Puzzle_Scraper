# sudoku decoder
# width/height from HTML are box dimensions (e.g. 3x3 for standard 9x9)
# actual grid is (width*height)^2
# encoding: digits=givens, letters a-z=empty cell gaps, underscores=separators


def decode(task_raw: str, width: int, height: int) -> dict:
    # calculate actual grid size from box dimensions
    grid_size = width * height
    total = grid_size * grid_size
    cells = []
    given_count = 0

    for ch in task_raw:
        if ch.isdigit():
            # given cell value
            cells.append(int(ch))
            given_count += 1
        elif ch.islower():
            # gap of empty cells (a=1, b=2, ... z=26)
            gap = ord(ch) - ord("a") + 1
            cells.extend([0] * gap)
        elif ch == "_":
            # separator between adjacent digits, no cell emitted
            pass
        else:
            raise ValueError(f"Unexpected character '{ch}' in task string")

    if len(cells) != total:
        raise ValueError(
            f"Decoded {len(cells)} cells but grid is {grid_size}x{grid_size}={total}"
        )

    # split flat list into comma-separated rows
    grid = []
    for row in range(grid_size):
        start = row * grid_size
        grid.append(",".join(str(c) for c in cells[start : start + grid_size]))

    return {
        "grid": grid,
        "given_count": given_count,
    }
