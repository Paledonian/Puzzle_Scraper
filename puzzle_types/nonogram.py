# nonogram clue decoder
# '/' separates clue groups, '.' separates numbers within a group
# first `width` groups = column clues, next `height` groups = row clues


def decode(task_raw: str, width: int, height: int) -> dict:
    parts = task_raw.split("/")
    expected = width + height
    if len(parts) != expected:
        raise ValueError(
            f"Expected {expected} clue groups ({width}+{height}), got {len(parts)}"
        )

    # convert '.' separators to ',' for readability
    column_clues = [p.replace(".", ",") for p in parts[:width]]
    row_clues = [p.replace(".", ",") for p in parts[width:]]

    return {
        "width": width,
        "height": height,
        "column_clues": column_clues,
        "row_clues": row_clues,
    }
