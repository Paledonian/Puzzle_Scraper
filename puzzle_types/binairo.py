# RLE decoder for binairo grids
# letters a-z = skip that many empty cells, digits = cell values


def decode_rle(raw: str, width: int, height: int) -> list[int]:
    total = width * height
    cells = []
    for ch in raw:
        if ch.islower():
            # letter = gap of empty cells (a=1, b=2, ... z=26)
            skip = ord(ch) - ord("a") + 1
            cells.extend([-1] * skip)
        elif ch.isdigit():
            cells.append(int(ch))
        else:
            raise ValueError(f"Unexpected character '{ch}' in task string")

    if len(cells) > total:
        raise ValueError(
            f"Decoded {len(cells)} cells but grid is {width}x{height}={total}"
        )

    # pad remaining cells as empty (-1) if the string ended early
    cells.extend([-1] * (total - len(cells)))
    return cells


def cells_to_rows(cells: list[int], width: int, height: int) -> list[str]:
    # convert flat cell list to row strings, -1 becomes '.' (empty)
    rows = []
    for row in range(height):
        start = row * width
        row_cells = cells[start : start + width]
        rows.append("".join("." if c == -1 else str(c) for c in row_cells))
    return rows


def decode(task_raw: str, width: int, height: int) -> dict:
    cells = decode_rle(task_raw, width, height)
    return {"size": width, "grid": cells_to_rows(cells, width, height)}
