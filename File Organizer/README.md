# Automated File Organizer

A Python script that scans an unorganized directory and sorts files into subdirectories based on their file extension.

## Requirements

- Target directory scanning: inspect files and classify them into destination subfolders (such as Documents, Images, Code, Archives).
- Safe file operations: never overwrite an existing file at destination. When a filename collision occurs, append a counter or timestamp.
- Console feedback: log every move operation showing filename, source path, and destination path.
- Edge case handling: handle missing read/write permissions, empty folders, and duplicate filenames without crashing.

## Tech stack

- Python 
- Standard library modules: `pathlib`, `shutil`, `os`

## Usage

```bash
python organizer.py --path "/path/to/target/folder"
```

## Planned improvements

- Logging to a local file instead of console stdout only.
- Dry-run mode (`--dry-run`) to preview file relocations before making changes on disk.
- Automation via cron (Linux) or Task Scheduler (Windows).
