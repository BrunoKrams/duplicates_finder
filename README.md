# Duplicate File Detector

[![License](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/mit)

This tool scans a directory tree and prints duplicate files.

It uses a two-step strategy:
1. Group files by size (fast pre-filter).
2. Hash only same-size candidates with SHA-256 (exact check).

This keeps the scan accurate while avoiding unnecessary hashing work.

## Features

- Recursively scans a directory.
- Handles disappearing files safely during grouping.
- Prints duplicate groups by SHA-256 hash.

## Requirements

- Python 3.10+
- No third-party dependencies

## Usage

Run from the project folder:

```bash
python main.py /path/to/directory
```

### Help

```bash
python main.py --help
```

## Input Validation

The script validates that the provided path:
- exists,
- is a directory,
- and is readable/traversable.

If validation fails, it exits.

## Example Output

```text
Collecting files in /tmp/demo
Collecting files in /tmp/demo/subdir
Classifying files by size
Classifying files of same size by full hash

2f6f4a...c0
/tmp/demo/a.txt
/tmp/demo/subdir/copy_of_a.txt
```

## Notes

- SHA-256 collisions are extremely unlikely, so matching hash groups are treated as duplicates.
- Very large trees can take time because file I/O dominates runtime.
- If files are modified while scanning, results may vary.

## Project Structure

- `main.py` - CLI entrypoint

