import hashlib
import os

from collections.abc import Callable, Iterable

def full_hash(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def size(file_path: str) -> str:
    return str(os.path.getsize(file_path))

def group(files: Iterable[str], classifier: Callable[[str], str]) -> dict[str, list[str]]:
    groups = {}
    for file in files:
        if not os.path.isfile(file):
            continue
        key = classifier(file)
        if key in groups:
            groups[key].append(file)
        else:
            groups[key] = [file]
    return groups

if __name__ == "__main__":
    memory_footprints = {}
    all_files = []
    for root, _, files in os.walk("/home/markus/hidrive"):
        print(f"Collecting files in {root}")
        for file in files:
            all_files.append(os.path.join(root, file))

    print("Classifying files by size")
    classified_by_size = group(all_files, size)
    for size, files in classified_by_size.items():
        print(size)
        for file in files:
            print(f"\t{file}")
    # same_size = {memory_footprint: files for memory_footprint, files in classified_by_size.items() if len(files) > 1}
    #
    # for size, files in same_size.items():
    #     print(size)
    #     for file_path in files:
    #         print("f\t{file_path}")