# tiny-tools

Small, single-file utilities that do one thing and stay out of the way.

No dependencies, no config files, no build step. Copy the file, run it, delete
it when you are done. Each tool is meant to be read in one sitting.

## What's inside

| Tool | What it does |
| --- | --- |
| [`linecount.py`](linecount.py) | Counts non-blank lines per file, sorted by size |

## linecount.py

Counts lines that actually contain something — blank lines and whitespace-only
lines are ignored, so the number reflects how much real content a tree holds.
Binary files and files over 2 MB are skipped, and common noise directories
(`.git`, `node_modules`, `__pycache__`, `dist`, …) are excluded by default.

```console
$ python linecount.py
   412  src/parser.py
   188  src/cli.py
    96  README.md
--------
   696  total non-blank lines in 3 files
```

Options:

```console
$ python linecount.py src docs      # scan specific paths
$ python linecount.py --top 5       # list only the five largest files
$ python linecount.py --all         # ignore the extension whitelist
```

It aims at source trees. For prose word counts you want a different tool.

## Why single files

A script that fits in one file is easy to audit, easy to paste into a container,
and impossible to break with a botched dependency upgrade. When a tool here
grows past a few hundred lines, it gets its own repository.

## License

MIT — see [LICENSE](LICENSE).
