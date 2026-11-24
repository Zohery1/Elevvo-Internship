#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import sys

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".md"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Video": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".json", ".sql"},
}


def log(message: str, log_file: str | None = None) -> None:
    print(message)
    if log_file:
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except OSError as e:
            print(f"warning: failed to write to {log_file}: {e}")


def get_destination_folder(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def get_unique_destination(dest_folder: Path, filename: str) -> Path:
    dest_path = dest_folder / filename
    if not dest_path.exists():
        return dest_path

    src = Path(filename)
    stem, suffix = src.stem, src.suffix
    counter = 1

    while True:
        candidate = dest_folder / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_directory(
    target_path: str | Path,
    dry_run: bool = False,
    log_file: str | None = "organizer.log",
) -> dict:
    target_dir = Path(target_path).resolve()
    stats = {"total": 0, "moved": 0, "renamed": 0, "errors": 0}

    if not target_dir.exists() or not target_dir.is_dir():
        log(f"error: invalid directory: {target_dir}", log_file)
        stats["errors"] += 1
        return stats

    if not os.access(target_dir, os.R_OK):
        log(f"error: read permission denied: {target_dir}", log_file)
        stats["errors"] += 1
        return stats

    if not dry_run and not os.access(target_dir, os.W_OK):
        log(f"error: write permission denied: {target_dir}", log_file)
        stats["errors"] += 1
        return stats

    current_script = Path(__file__).resolve()
    log_path = Path(log_file).resolve() if log_file else None

    try:
        entries = list(target_dir.iterdir())
    except PermissionError as e:
        log(f"error: permission denied accessing {target_dir}: {e}", log_file)
        stats["errors"] += 1
        return stats

    files = [
        f for f in entries
        if f.is_file() and f != current_script and (log_path is None or f != log_path)
    ]
    stats["total"] = len(files)

    if not files:
        log(f"No files to organize in {target_dir}", log_file)
        return stats

    log(f"\nOrganizing {target_dir} ({len(files)} files)", log_file)
    if dry_run:
        log("dry-run: preview only, files will not be moved", log_file)

    for file_path in sorted(files, key=lambda f: f.name.lower()):
        if not os.access(file_path, os.R_OK):
            log(f"error: cannot read {file_path.name}, skipping", log_file)
            stats["errors"] += 1
            continue

        folder_name = get_destination_folder(file_path)
        dest_folder = target_dir / folder_name
        dest_file = get_unique_destination(dest_folder, file_path.name)
        was_renamed = dest_file.name != file_path.name

        if was_renamed:
            stats["renamed"] += 1
            note = f" (renamed to {dest_file.name})"
        else:
            note = ""

        prefix = "dry-run: would move" if dry_run else "moved"
        log(f"{prefix}: {file_path.name} -> {folder_name}/{dest_file.name}{note}", log_file)

        if not dry_run:
            try:
                dest_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest_file))
                stats["moved"] += 1
            except (PermissionError, OSError) as e:
                log(f"error: failed to move {file_path.name}: {e}", log_file)
                stats["errors"] += 1
        else:
            stats["moved"] += 1

    log(
        f"\nDone: {stats['moved']}/{stats['total']} moved, "
        f"{stats['renamed']} renamed, {stats['errors']} errors\n",
        log_file,
    )
    return stats


def main() -> None:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args or "-d" in args
    paths = [a for a in args if a not in ("--dry-run", "-d")]

    target = paths[0] if paths else input("Directory to organize (default: . ) : ").strip() or "."
    organize_directory(target, dry_run=dry_run, log_file="organizer.log")


if __name__ == "__main__":
    main()
