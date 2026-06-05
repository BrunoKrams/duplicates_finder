import hashlib
import logging
import os
import argparse
from pathlib import Path

from collections.abc import Callable, Iterable

logger = logging.getLogger("DuplicatesFinder")

def full_hash(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def size(file_path: str) -> str:
    return str(os.path.getsize(file_path))


def group(files: Iterable[str], classifier: Callable[[str], str]) -> dict[str, list[str]]:
    files = list(files)
    total_files = len(files)
    logger.info("Grouping %d files", total_files)

    groups = {}
    for index, file in enumerate(files, start=1):
        logger.info("Analyzing file %d/%d", index, total_files)
        if not os.path.isfile(file):
            continue
        key = classifier(file)
        if key in groups:
            groups[key].append(file)
        else:
            groups[key] = [file]
    return groups


def parse_directory(raw_path: str) -> str:
    path = Path(raw_path).expanduser()
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Path does not exist: {raw_path}")
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"Path is not a directory: {raw_path}")

    resolved_path = path.resolve()
    if not os.access(resolved_path, os.R_OK | os.X_OK):
        raise argparse.ArgumentTypeError(f"Directory is not readable/traversable: {raw_path}")
    return str(resolved_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find duplicate files by grouping by size and then full SHA-256 hash."
    )
    parser.add_argument(
        "directory",
        type=parse_directory,
        help="Directory to scan for duplicate files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root_directory = args.directory

    all_files: list[str] = []
    for root, _, files in os.walk(root_directory):
        print(f"Collecting files in {root}")
        for file in files:
            all_files.append(os.path.join(root, file))

    print("Classifying files by size")
    classified_by_size = group(all_files, size)
    candidates = [file for _, files in classified_by_size.items() if len(files) > 1 for file in files]

    print("Classifying files of same size by full hash")
    classified_by_full_hash = group(candidates, full_hash)
    duplicates = {file_hash: files for file_hash, files in classified_by_full_hash.items() if len(files) > 1}

    if not duplicates:
        logger.info(f"No duplicates found in {root_directory}")
    else:
        logger.info(f"The following files seem to be duplicates")
        for file_hash, files in duplicates.items():
            print()
            print(f"Hash: {file_hash}")
            for file in files:
                print(f"\t{file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
