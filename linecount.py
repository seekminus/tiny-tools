#!/usr/bin/env python3
"""linecount - count non-blank lines in source files.

One file, no dependencies. Useful when you want to know how much of a tree is
actual content versus whitespace.

Usage:
    python linecount.py                # scan current directory
    python linecount.py src docs       # scan specific paths
    python linecount.py --top 5        # show only the 5 biggest files
    python linecount.py --all          # ignore the extension whitelist
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules", ".venv", "venv",
    "dist", "build", ".mypy_cache", ".pytest_cache", ".idea", ".vscode",
}

TEXT_EXTS = {
    ".py", ".md", ".txt", ".rst", ".sh", ".bash", ".zsh",
    ".js", ".jsx", ".ts", ".tsx", ".css", ".html",
    ".go", ".rs", ".java", ".kt", ".c", ".h", ".cpp",
    ".sql", ".yml", ".yaml", ".toml", ".ini", ".json", ".cfg",
}

MAX_BYTES = 2 * 1024 * 1024  # skip anything obviously not source


def iter_files(roots: list[Path], every_ext: bool):
    """Yield candidate files, skipping noisy directories."""
    for root in roots:
        if root.is_file():
            yield root
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if not every_ext and path.suffix.lower() not in TEXT_EXTS:
                continue
            yield path


def count_lines(path: Path) -> int | None:
    """Non-blank line count, or None when the file is unreadable/binary."""
    try:
        if path.stat().st_size > MAX_BYTES:
            return None
        text = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeDecodeError):
        return None
    return sum(1 for line in text.splitlines() if line.strip())


def human(n: int) -> str:
    return f"{n:,}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="linecount",
        description="Count non-blank lines in source files.",
    )
    parser.add_argument("paths", nargs="*", default=["."], help="files or directories (default: .)")
    parser.add_argument("--top", type=int, default=20, help="how many files to list (default: 20)")
    parser.add_argument("--all", action="store_true", help="scan every extension, not just source")
    args = parser.parse_args(argv)

    roots = [Path(p) for p in args.paths]
    missing = [str(p) for p in roots if not p.exists()]
    if missing:
        print(f"no such path: {', '.join(missing)}", file=sys.stderr)
        return 2

    results: list[tuple[int, Path]] = []
    skipped = 0
    for path in iter_files(roots, args.all):
        n = count_lines(path)
        if n is None:
            skipped += 1
            continue
        results.append((n, path))

    if not results:
        print("nothing to count")
        return 0

    results.sort(reverse=True)
    total = sum(n for n, _ in results)
    width = max(len(human(n)) for n, _ in results)

    for n, path in results[: max(args.top, 0)]:
        print(f"{human(n):>{width}}  {path}")

    if len(results) > args.top:
        hidden = len(results) - args.top
        print(f"{'...':>{width}}  ({hidden} more files)")

    print(f"{'-' * (width + 2)}")
    print(f"{human(total):>{width}}  total non-blank lines in {human(len(results))} files")
    if skipped:
        print(f"{'':>{width}}  ({human(skipped)} skipped: binary or unreadable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
