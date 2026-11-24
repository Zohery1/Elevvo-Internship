# File Organizer

A Python script that sorts loose files in a directory into subfolders based on their extension (Images, Documents, Audio, Video, Archives, Code).

## Features

- Moves files into subfolders by category.
- Avoids overwriting existing files: if a file with the same name already exists in the destination, it appends a number (such as `notes.txt` to `notes_1.txt`).
- Skips subdirectories, the script file, and the log file.
- Handles unreadable files, missing permissions, and empty folders without crashing.
- Logs move operations to the console and appends details to `organizer.log`.
- Includes a `--dry-run` flag to preview moves before changing anything on disk.
- Built using only Python standard library modules (`os`, `shutil`, `pathlib`, `sys`).

## Usage

Organize a specific directory:

```bash
python files.py "/path/to/folder"
```

If run without arguments, the script prompts for a directory path:

```bash
python files.py
```

Preview changes without moving any files:

```bash
python files.py "/path/to/folder" --dry-run
```

## Running tests

```bash
python -m unittest test_organizer.py
```

## Scheduled runs

### Linux and macOS (cron)

To run the script every day at 10:00 PM:

```bash
crontab -e
```

Add:

```cron
0 22 * * * /usr/bin/python3 "/path/to/File Organizer/files.py" "/path/to/Downloads"
```

### Windows (Task Scheduler)

1. Open Task Scheduler (`taskschd.msc`).
2. Create a basic task with a daily trigger.
3. Under Action, select "Start a program":
   - Program/script: `python.exe`
   - Arguments: `"C:\path\to\File Organizer\files.py" "C:\Users\username\Downloads"`
