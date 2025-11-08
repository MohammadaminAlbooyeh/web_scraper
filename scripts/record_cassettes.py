"""Record vcrpy cassettes for key pages used in tests.

Usage:
    python scripts/record_cassettes.py --mode once
    python scripts/record_cassettes.py --commit "Add new cassettes"

Options:
    --mode {all,once,none}   vcrpy record_mode (default: once)
    --commit MESSAGE         If provided, run `git add` and `git commit -m MESSAGE`

Note: this script performs live HTTP requests. Use respectfully and avoid
excessive runs against remote sites.
"""
import argparse
import subprocess
from pathlib import Path

import requests
import vcr


CASSETTE_DIR = Path(__file__).parent.parent / "tests" / "fixtures" / "cassettes"
CASSETTE_DIR.mkdir(parents=True, exist_ok=True)

URLS = {
    "books_listing": "http://books.toscrape.com/",
    "sample_product": "http://books.toscrape.com/catalogue/sample-book_1/index.html",
}


def record_cassettes(record_mode: str = "once"):
    my_vcr = vcr.VCR(
        serializer="yaml",
        cassette_library_dir=str(CASSETTE_DIR),
        record_mode=record_mode,
        match_on=["uri", "method"],
    )

    for name, url in URLS.items():
        cassette_path = CASSETTE_DIR / f"{name}.yaml"
        print(f"Recording cassette {cassette_path} (mode={record_mode}) from {url}")
        with my_vcr.use_cassette(cassette_path.name):
            r = requests.get(url, timeout=30)
            print(f"  -> {r.status_code} {r.reason}")


def git_commit_cassettes(message: str):
    # Stage new/updated cassette files and commit them
    try:
        subprocess.run(["git", "add", str(CASSETTE_DIR)], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        print("Committed cassettes to git")
    except subprocess.CalledProcessError as e:
        print("Git commit failed:", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["all", "once", "none"], default="once")
    parser.add_argument("--commit", help="Commit message to use when committing cassettes (optional)")
    args = parser.parse_args()

    record_cassettes(args.mode)

    if args.commit:
        git_commit_cassettes(args.commit)


if __name__ == "__main__":
    main()
