# hashi (bridges) RLE decoder
# digits = islands, letters a-z = empty cell gaps


def decode(task_raw: str, width: int, height: int) -> dict:
    total = width * height
    cells = []
    island_count = 0

    for ch in task_raw:
        if ch.isdigit():
            # digit = island with that many required bridge connections
            cells.append(int(ch))
            island_count += 1
        elif ch.islower():
            # letter = gap of empty cells (a=1, b=2, ... z=26)
            gap = ord(ch) - ord("a") + 1
            cells.extend([0] * gap)
        else:
            raise ValueError(f"Unexpected character '{ch}' in task string")

    if len(cells) != total:
        raise ValueError(
            f"Decoded {len(cells)} cells but grid is {width}x{height}={total}"
        )

    # split flat list into comma-separated rows
    grid = []
    for row in range(height):
        start = row * width
        grid.append(",".join(str(c) for c in cells[start : start + width]))

    return {
        "size": width,
        "grid": grid,
        "island_count": island_count,
    }
