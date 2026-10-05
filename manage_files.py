#!/usr/bin/env python3
"""
=============================================================================
Repository File Organizer & Workspace Manager
=============================================================================
This script automatically organizes loose assets and documents in the project
root directory into structured categories under 'File Management/'.

Usage:
    python manage_files.py

Anyone who clones this repository can run this script independently on any
machine (Windows, macOS, Linux) without needing any AI assistant or external
dependencies.
=============================================================================
"""

import os
import shutil
import sys
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
TARGET_BASE = BASE_DIR / "File Management"

# Protected items that MUST remain in the root directory
PROTECTED_NAMES = {
    "docker-compose.yml",
    "docker-compose.yaml",
    "manage_files.py",
    "README.md",
    "LICENSE",
    ".gitignore",
    ".dockerignore",
    ".env",
    "extra-addons",
    "File Management",
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".vscode",
    ".idea",
}

# Category folder mappings based on extensions and keywords
EXTENSION_MAPPING = {
    ".docx": "DOCX",
    ".doc": "DOCX",
    ".pptx": "Presentation",
    ".ppt": "Presentation",
    ".puml": "Diagrams",
    ".drawio": "Diagrams",
    ".txt": "Others",
}


def is_protected(path: Path) -> bool:
    """Checks if a file or folder is protected from being moved."""
    name = path.name
    if name in PROTECTED_NAMES:
        return True
    if name.startswith("~$"):  # Temporary Word/Office lock files
        return True
    if name.startswith("."):
        return True
    return False


def get_target_subfolder(path: Path) -> str:
    """Determines the appropriate subfolder in 'File Management/' for a file."""
    ext = path.suffix.lower()
    name_lower = path.name.lower()

    # Specialized logic for PDFs
    if ext == ".pdf":
        if any(k in name_lower for k in ["presentation", "slide", "pitch", "deck"]):
            return "Presentation"
        return "PDFs"

    # Specialized logic for HTML presentations
    if ext == ".html" and "presentation" in name_lower:
        return "Presentation"

    # Markdown documentation (except root README.md)
    if ext == ".md" and name_lower != "readme.md":
        return ".md"

    # Python scripts in root or scratch (except this runner)
    if ext == ".py" and path.name != "manage_files.py":
        return "Scripts"

    # Default extension lookup
    return EXTENSION_MAPPING.get(ext, "Others")


def organize_workspace():
    """Scans root directory and moves loose assets into 'File Management/'."""
    print("=" * 65)
    print(">> Workspace File Manager")
    print(f"   Root Directory: {BASE_DIR}")
    print(f"   Destination:    {TARGET_BASE}")
    print("=" * 65)

    TARGET_BASE.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    skipped_count = 0

    # 1. Process loose files in the root directory
    for item in sorted(BASE_DIR.iterdir()):
        if item.is_dir():
            # Check scratch folder specifically
            if item.name == "scratch":
                for scratch_file in item.iterdir():
                    if scratch_file.is_file() and not is_protected(scratch_file):
                        dest_sub = get_target_subfolder(scratch_file)
                        dest_dir = TARGET_BASE / dest_sub
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        dest_file = dest_dir / scratch_file.name

                        try:
                            shutil.move(str(scratch_file), str(dest_file))
                            print(f"  [MOVED] scratch/{scratch_file.name} -> File Management/{dest_sub}/")
                            moved_count += 1
                        except Exception as e:
                            print(f"  [ERROR] Could not move {scratch_file.name}: {e}")

                # Clean up empty scratch folder
                try:
                    if not any(item.iterdir()):
                        item.rmdir()
                        print("  [CLEAN] Removed empty scratch directory")
                except Exception:
                    pass
            continue

        if not item.is_file():
            continue

        if is_protected(item):
            continue

        dest_sub = get_target_subfolder(item)
        dest_dir = TARGET_BASE / dest_sub
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / item.name

        try:
            # If the destination file already exists and is identical, remove root copy
            if dest_file.exists():
                if dest_file.stat().st_size == item.stat().st_size:
                    item.unlink()
                    print(f"  [CLEAN] Removed duplicate {item.name} (already in File Management/{dest_sub}/)")
                    moved_count += 1
                    continue
                else:
                    # Rename with duplicate suffix if different
                    dest_file = dest_dir / f"{item.stem}_new{item.suffix}"

            shutil.move(str(item), str(dest_file))
            print(f"  [MOVED] {item.name} -> File Management/{dest_sub}/")
            moved_count += 1

        except PermissionError:
            print(f"  [LOCKED] {item.name} is currently open by another application (skipped)")
            skipped_count += 1
        except Exception as e:
            print(f"  [ERROR] Could not move {item.name}: {e}")
            skipped_count += 1

    print("-" * 65)
    print(f"Organization complete! ({moved_count} organized, {skipped_count} skipped/protected)")
    print("=" * 65)


if __name__ == "__main__":
    organize_workspace()
