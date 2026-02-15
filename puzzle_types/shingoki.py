# shingoki decoder
# played on dot intersections so grid is (width+1) x (height+1)
# token format: [B|W][digits][lowercase letters]
#   B/W = circle type (black=straight path, white=turn)
#   digits = clue value
#   trailing letters = gap of empty dots (letters are summed, e.g. 'zh' = 26+8 = 34)


def decode(task_raw: str, width: int, height: int) -> dict:
    # dot grid is one larger than the cell grid in each dimension
    cols = width + 1
    rows = height + 1
    total = rows * cols
    cells = ["."] * total
    pos = 0
    i = 0

    while i < len(task_raw):
        ch = task_raw[i]
        if ch not in ("B", "W"):
            raise ValueError(f"Expected 'B' or 'W' at position {i}, got '{ch}'")

        # read circle type
        circle_type = ch
        i += 1

        # read the clue number
        num_str = ""
        while i < len(task_raw) and task_raw[i].isdigit():
            num_str += task_raw[i]
            i += 1
        value = int(num_str)

        # read trailing gap letters (multiple letters are summed)
        empties = 0
        while i < len(task_raw) and task_raw[i].islower():
            empties += ord(task_raw[i]) - ord("a") + 1
            i += 1

        # place circle at current position, then skip over empty dots
        cells[pos] = f"{circle_type}{value}"
        pos += 1 + empties

    if pos != total:
        raise ValueError(
            f"Final position {pos} != {cols}x{rows}={total}"
        )

    # split flat list into comma-separated rows
    grid = []
    for row in range(rows):
        start = row * cols
        grid.append(",".join(cells[start : start + cols]))

    return {
        "size": width,
        "grid": grid,
    }
