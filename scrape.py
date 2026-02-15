import importlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

from config import PUZZLES

# puzzles/ sits one level above scraper/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# regex patterns to pull task data from the puzzle page's JavaScript
TASK_PATTERN = re.compile(r'var\s+task\s*=\s*["\']([^"\']+)["\']')
SIZE_PATTERN = re.compile(r"puzzleWidth:\s*(\d+).*?puzzleHeight:\s*(\d+)", re.DOTALL)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def extract_task(html: str) -> str:
    # find var task = '...' in the page source
    match = TASK_PATTERN.search(html)
    if not match:
        raise ValueError("Could not find 'var task' in page HTML")
    return match.group(1)


def extract_size(html: str) -> tuple[int, int]:
    # find puzzleWidth and puzzleHeight in the page source
    match = SIZE_PATTERN.search(html)
    if not match:
        raise ValueError("Could not find puzzleWidth/puzzleHeight in page HTML")
    return int(match.group(1)), int(match.group(2))


def scrape_puzzle(name: str, cfg: dict) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_dir = PROJECT_ROOT / cfg["output_folder"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{today}.json"

    # skip if already scraped today
    if output_file.exists():
        print(f"[{name}] {today}.json already exists, skipping.")
        return

    print(f"[{name}] Scraping puzzle for {today}...")

    # fetch the puzzle page
    try:
        resp = requests.get(
            cfg["url"], headers={"User-Agent": USER_AGENT}, timeout=30
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[{name}] Network error: {e}")
        return

    # extract the encoded task string and grid dimensions from HTML
    try:
        task_raw = extract_task(resp.text)
        width, height = extract_size(resp.text)
    except ValueError as e:
        print(f"[{name}] Parse error: {e}")
        return

    # dynamically import the right decoder and decode the task string
    try:
        module = importlib.import_module(f"puzzle_types.{cfg['puzzle_type']}")
        result = module.decode(task_raw, width, height)
    except Exception as e:
        print(f"[{name}] Decode error: {e}")
        return

    # combine metadata with decoded puzzle data and save
    data = {
        "date": today,
        "puzzle": name,
        **result,
    }

    output_file.write_text(json.dumps(data, indent=4), encoding="utf-8")
    print(f"[{name}] Saved {output_file}")


def main():
    # allow scraping specific puzzles by name, or all if none specified
    if len(sys.argv) > 1:
        names = sys.argv[1:]
        for name in names:
            if name not in PUZZLES:
                print(f"Unknown puzzle: {name}")
                print(f"Available: {', '.join(PUZZLES)}")
                sys.exit(1)
    else:
        names = list(PUZZLES)

    for name in names:
        scrape_puzzle(name, PUZZLES[name])


if __name__ == "__main__":
    main()
