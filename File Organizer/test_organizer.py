#!/usr/bin/env python3
from pathlib import Path
import shutil
import tempfile
import unittest

from files import (
    get_destination_folder,
    get_unique_destination,
    organize_directory,
)


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.log_file = str(self.test_dir / "test_organizer.log")

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_get_destination_folder(self):
        self.assertEqual(get_destination_folder(Path("sample.jpg")), "Images")
        self.assertEqual(get_destination_folder(Path("doc.pdf")), "Documents")
        self.assertEqual(get_destination_folder(Path("track.mp3")), "Audio")
        self.assertEqual(get_destination_folder(Path("clip.mp4")), "Video")
        self.assertEqual(get_destination_folder(Path("data.zip")), "Archives")
        self.assertEqual(get_destination_folder(Path("main.py")), "Code")
        self.assertEqual(get_destination_folder(Path("unknown.xyz")), "Others")
        self.assertEqual(get_destination_folder(Path("no_extension")), "Others")

    def test_unique_destination_without_collision(self):
        dest_folder = self.test_dir / "Documents"
        dest_folder.mkdir()
        dest_path = get_unique_destination(dest_folder, "report.pdf")
        self.assertEqual(dest_path.name, "report.pdf")

    def test_unique_destination_with_collision(self):
        dest_folder = self.test_dir / "Documents"
        dest_folder.mkdir()

        (dest_folder / "report.pdf").write_text("first")
        (dest_folder / "report_1.pdf").write_text("second")

        dest_path = get_unique_destination(dest_folder, "report.pdf")
        self.assertEqual(dest_path.name, "report_2.pdf")

    def test_dry_run_does_not_move_files(self):
        test_file = self.test_dir / "photo.png"
        test_file.write_text("content")

        stats = organize_directory(self.test_dir, dry_run=True, log_file=self.log_file)

        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["moved"], 1)
        self.assertTrue(test_file.exists())
        self.assertFalse((self.test_dir / "Images").exists())

    def test_live_organization_and_collision_prevention(self):
        images_dir = self.test_dir / "Images"
        images_dir.mkdir()
        (images_dir / "photo.png").write_text("existing original")

        (self.test_dir / "photo.png").write_text("incoming new")
        (self.test_dir / "notes.txt").write_text("text notes")

        stats = organize_directory(self.test_dir, dry_run=False, log_file=self.log_file)

        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["moved"], 2)
        self.assertEqual(stats["renamed"], 1)

        self.assertEqual((images_dir / "photo.png").read_text(), "existing original")
        self.assertTrue((images_dir / "photo_1.png").exists())
        self.assertEqual((images_dir / "photo_1.png").read_text(), "incoming new")
        self.assertTrue((self.test_dir / "Documents" / "notes.txt").exists())

        log_content = Path(self.log_file).read_text(encoding="utf-8")
        self.assertIn("renamed to photo_1.png", log_content)
        self.assertIn("Done:", log_content)

    def test_empty_folder(self):
        stats = organize_directory(self.test_dir, dry_run=False, log_file=self.log_file)
        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["errors"], 0)


if __name__ == "__main__":
    unittest.main()
