# decodes a hex pipe grid where edges wrap around (connect to the opposite side)
from puzzle_types.pipes import decode as _pipes_decode


def decode(task_raw: str, width: int, height: int) -> dict:
    result = _pipes_decode(task_raw, width, height)
    result["wrap"] = True
    return result
