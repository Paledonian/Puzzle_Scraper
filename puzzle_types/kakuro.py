# kakuro decoder
# tokens: B=wall, _=separator, digits+letter=clue+empties, bare digits=down-only clue


def decode(task_raw: str, width: int, height: int) -> dict:
    total = width * height
    cells = []
    i = 0

    while i < len(task_raw):
        ch = task_raw[i]

        if ch == "B":
            # wall / black cell
            cells.append("X")
            i += 1

        elif ch == "_":
            # separator between adjacent tokens, no cell emitted
            i += 1

        elif ch.isdigit():
            # collect all consecutive digits
            num_str = ""
            while i < len(task_raw) and task_raw[i].isdigit():
                num_str += task_raw[i]
                i += 1

            if i < len(task_raw) and task_raw[i].islower():
                # digits followed by letter = clue cell + trailing empty cells
                letter = task_raw[i]
                i += 1
                empties = ord(letter) - ord("a") + 1

                # last 2 digits = down clue, leading digits = right clue
                down = int(num_str[-2:])
                right = int(num_str[:-2]) if len(num_str) > 2 else 0

                # format clue as d/r combination
                if right > 0 and down > 0:
                    cells.append(f"d{down}r{right}")
                elif right > 0:
                    cells.append(f"r{right}")
                elif down > 0:
                    cells.append(f"d{down}")
                else:
                    cells.append("X")

                # add the trailing empty cells
                cells.extend(["."] * empties)
            else:
                # bare number with no letter = down-only clue
                cells.append(f"d{int(num_str)}")

        else:
            raise ValueError(f"Unexpected character '{ch}' at position {i}")

    if len(cells) != total:
        raise ValueError(
            f"Decoded {len(cells)} cells but grid is {width}x{height}={total}"
        )

    # split flat list into comma-separated rows
    grid = []
    for row in range(height):
        start = row * width
        grid.append(",".join(cells[start : start + width]))

    return {
        "size": width,
        "grid": grid,
    }
