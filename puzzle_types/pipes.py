# each cell in the task string is a single hex digit (0-f)
# representing the pipe type at that position


def decode(task_raw: str, width: int, height: int) -> dict:
    total = width * height
    if len(task_raw) != total:
        raise ValueError(
            f"Task string length {len(task_raw)} != {width}x{height}={total}"
        )

    # convert each hex character to its integer value
    cells = [int(ch, 16) for ch in task_raw]

    # split flat list into comma-separated rows
    grid = []
    for row in range(height):
        start = row * width
        grid.append(",".join(str(c) for c in cells[start : start + width]))

    return {"size": width, "grid": grid}
