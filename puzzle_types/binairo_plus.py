# binairo+ task string contains two RLE grids separated by '|'
# first half = given cell values, second half = constraint markers

from puzzle_types.binairo import cells_to_rows, decode_rle


def decode(task_raw: str, width: int, height: int) -> dict:
    # split task string into the cell grid and constraint grid
    grid_raw, constraint_raw = task_raw.split("|", 1)

    grid = cells_to_rows(decode_rle(grid_raw, width, height), width, height)
    constraints = cells_to_rows(decode_rle(constraint_raw, width, height), width, height)

    return {"size": width, "grid": grid, "constraints": constraints}
