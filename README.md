# Puzzle Scraper

Scrapes daily puzzles from `puzzle-*.com` sites and saves them as structured JSON files.

Designed to run on a server via cron job. Scraped puzzles are stored locally and synced to other devices via Syncthing.

## Supported Puzzles

| Puzzle | Source | Daily URL |
|--------|--------|-----------|
| Binairo | [puzzle-binairo.com](https://www.puzzle-binairo.com/daily-binairo/) | `/daily-binairo/` |
| Binairo+ | [puzzle-binairo.com](https://www.puzzle-binairo.com/daily-binairo-plus/) | `/daily-binairo-plus/` |
| Pipes | [puzzle-pipes.com](https://www.puzzle-pipes.com/?size=7) | `?size=7` |
| Pipes Wrap | [puzzle-pipes.com](https://www.puzzle-pipes.com/?size=17) | `?size=17` |
| Hashi | [puzzle-bridges.com](https://www.puzzle-bridges.com/?size=13) | `?size=13` |
| Kakuro | [puzzle-kakuro.com](https://www.puzzle-kakuro.com/?size=15) | `?size=15` |
| Nonogram | [puzzle-nonograms.com](https://www.puzzle-nonograms.com/?size=6) | `?size=6` |
| Shingoki | [puzzle-shingoki.com](https://www.puzzle-shingoki.com/?size=17) | `?size=17` |
| Sudoku | [puzzle-sudoku.com](https://www.puzzle-sudoku.com/?size=9) | `?size=9` |

## Usage

```bash
# Scrape all puzzles
python scrape.py

# Scrape specific puzzles
python scrape.py hashi sudoku pipes
```

If today's JSON already exists for a puzzle, it is skipped automatically.

## How It Works

All the puzzle sites (`puzzle-binairo.com`, `puzzle-pipes.com`, etc.) are built the same way. When you visit a puzzle page, the HTML contains the puzzle data as an encoded string and the grid dimensions. Every site uses the same pattern, which means one scraper can handle all of them.

The scraper does four things for each puzzle:

1. **Downloads** the puzzle page
2. **Finds** the encoded puzzle string and grid size from the HTML
3. **Decodes** the puzzle string into a clean, readable format
4. **Saves** the result as a JSON file named by today's date

If today's file already exists, the puzzle is skipped so it's safe to run multiple times.

### File Structure

- **`scrape.py`** does steps 1, 2, and 4 (the parts that are the same for every puzzle)
- **`config.py`** lists all the puzzles with their URLs and where to save them
- **`puzzle_types/`** has one file per puzzle type (e.g. `hashi.py`, `sudoku.py`) that handles step 3 (decoding the puzzle string into structured data)

---

## Puzzle Data Formats

Every JSON file contains at minimum:

```json
{
    "date": "YYYY-MM-DD",
    "puzzle": "puzzle_name",
    ...
}
```

Additional fields are puzzle-specific.

---

### Binairo

Binary determination puzzle. Fill the grid with 0s and 1s.

**Rules:** Each row and column must contain equal numbers of 0s and 1s. No more than two consecutive identical digits in any row or column. No two rows or columns may be identical.

| Field | Description |
|-------|-------------|
| `size` | Grid dimension (e.g. 24 for 24x24) |
| `grid` | Array of strings, one per row |

**Grid cells:** `0` = white, `1` = black, `.` = empty

---

### Binairo+

Same as Binairo with additional pairwise constraints between adjacent cells.

| Field | Description |
|-------|-------------|
| `size` | Grid dimension |
| `grid` | Array of strings, one per row |
| `constraints` | Array of strings encoding adjacency constraints |

**Grid cells:** `0` = white, `1` = black, `.` = empty

**Constraint encoding:** Each character is `.` (none) or a digit 1-8 packing two constraints via `digit = (bottom x 3) + right`. Decode: `right = digit % 3`, `bottom = digit // 3`. Each gives 0 = none, 1 = equal, 2 = different.

| Digit | Right | Bottom |
|:-----:|:-----:|:------:|
| 1 | = | -- |
| 2 | x | -- |
| 3 | -- | = |
| 4 | = | = |
| 5 | x | = |
| 6 | -- | x |
| 7 | = | x |
| 8 | x | x |

---

### Pipes

Rotate pipe tiles to connect them all into a single loop-free network.

**Rules:** Rotate tiles so all pipes connect into a single connected group with no closed loops.

| Field | Description |
|-------|-------------|
| `size` | Grid dimension |
| `grid` | Array of comma-separated strings, pipe type integers 1-14 |

**Pipe encoding:** Each value is a direction bitmask: Right=1, Up=2, Left=4, Down=8.

| Type | Directions | Shape |
|:----:|:----------:|:-----:|
| 1 | R | dead end |
| 2 | U | dead end |
| 3 | U,R | L-bend |
| 4 | L | dead end |
| 5 | L,R | straight |
| 6 | U,L | L-bend |
| 7 | U,L,R | T-junction |
| 8 | D | dead end |
| 9 | D,R | L-bend |
| 10 | U,D | straight |
| 11 | U,D,R | T-junction |
| 12 | D,L | L-bend |
| 13 | D,L,R | T-junction |
| 14 | U,D,L | T-junction |

---

### Pipes Wrap

Same as Pipes but edges wrap around (torus topology).

| Field | Description |
|-------|-------------|
| `size` | Grid dimension |
| `grid` | Array of comma-separated strings, pipe type integers 1-14 |
| `wrap` | Always `true` |

Pipe encoding is identical to Pipes.

---

### Hashi (Bridges)

Connect numbered islands with bridges.

**Rules:** Connect islands with 1 or 2 bridges per connection. Bridges run horizontally or vertically and cannot cross. Each island's number equals its total bridge count. All islands must form a single connected group.

| Field | Description |
|-------|-------------|
| `size` | Grid dimension |
| `grid` | Array of comma-separated strings, one per row |
| `island_count` | Total number of islands |

**Grid cells:** `0` = empty, `1`-`8` = island requiring that many bridges

---

### Kakuro

Number crossword where clue cells show target sums.

**Rules:** Fill empty cells with digits 1-9. Each clue gives the sum for a consecutive run of cells. Within each run, all digits must be unique.

| Field | Description |
|-------|-------------|
| `size` | Grid dimension |
| `grid` | Array of comma-separated strings, one per row |

**Grid cells:**

| Value | Meaning |
|-------|---------|
| `X` | Wall (black cell) |
| `.` | Empty cell (fill with 1-9) |
| `d{N}` | Down-only clue (e.g. `d16`) |
| `r{N}` | Right-only clue (e.g. `r3`) |
| `d{N}r{M}` | Both clues (e.g. `d13r12`) |

---

### Nonogram

Picture logic puzzle. Fill cells based on row and column clues.

**Rules:** Numbers indicate groups of consecutive filled cells. Groups appear in the given order, separated by at least one empty cell.

| Field | Description |
|-------|-------------|
| `width` | Number of columns |
| `height` | Number of rows |
| `column_clues` | List of comma-separated strings, one per column |
| `row_clues` | List of comma-separated strings, one per row |

Each clue string like `"5,3,1"` means groups of 5, 3, and 1 filled cells in order.

---

### Shingoki

Loop-drawing puzzle on a grid of intersection points.

**Rules:** Draw a single closed loop through the dots. The loop passes through every circle. Black circles require a straight pass-through. White circles require a 90-degree turn. The number on a circle is the total length of straight segments through it. The loop cannot cross or branch.

| Field | Description |
|-------|-------------|
| `size` | Cell grid dimension (dot grid is size+1 per side) |
| `grid` | Array of comma-separated strings, one per row of the dot grid |

**Grid cells:** `.` = empty dot, `B{N}` = black circle (straight), `W{N}` = white circle (turn)

Note: The dot grid has (size+1) rows and (size+1) columns.

---

### Sudoku

Classic number placement puzzle.

**Rules:** Fill the grid so every row, column, and box contains digits 1 through N exactly once (N = box_width x box_height, typically 9).

| Field | Description |
|-------|-------------|
| `grid` | Array of comma-separated strings, one per row |
| `given_count` | Number of pre-filled cells |

**Grid cells:** `0` = empty, `1`-`9` = given (pre-filled)
