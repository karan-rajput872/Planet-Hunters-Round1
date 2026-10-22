"""
Creates the clean, portfolio-ready standalone distribution archive.
Includes code, tests, docs, scripts, submissions, and visual assets.
Excludes large datasets (.npy), environment (.venv), and caches.
"""
import zipfile
from pathlib import Path

dist_dir = Path("dist")
dist_dir.mkdir(parents=True, exist_ok=True)
zip_path = dist_dir / "Planet-Hunters-Round1-Portfolio-Ready.zip"

include_patterns = [
    "README.md",
    "CHANGELOG.md",
    "LICENSE_STATUS.md",
    "pyproject.toml",
    "requirements.txt",
    ".gitignore",
    ".gitattributes",
    "train.py",
    "generate_submission.py",
    "validate_submission.py",
    "src/**/*.py",
    "tests/**/*.py",
    "docs/**/*.md",
    "assets/**/*.png",
    "reports/**/*.md",
    "reports/**/*.csv",
    "reports/**/*.png",
    "reports/**/*.txt",
    "scripts/**/*.py",
    "submissions/**/*.csv",
    "notebooks/**/*.ipynb",
    "data/**/.gitkeep",
    "models/**/.gitkeep"
]

print(f"Creating portfolio distribution archive: {zip_path}...")

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
    added_files = set()
    for pattern in include_patterns:
        for p in Path(".").glob(pattern):
            if p.is_file() and p not in added_files:
                # Do not include anything inside .venv, __pycache__, or dist
                if any(part in p.parts for part in [".venv", "__pycache__", "dist", ".git"]):
                    continue
                zipf.write(p, arcname=p.as_posix())
                added_files.add(p)

print(f"[SUCCESS] Packaged {len(added_files)} files into {zip_path}")
print(f"Archive Size: {zip_path.stat().st_size / (1024 * 1024):.2f} MB")

# Verify archive
with zipfile.ZipFile(zip_path, "r") as zipf:
    test_result = zipf.testzip()
    namelist = zipf.namelist()
    if test_result is None:
        print(f"[VERIFY] Archive integrity verified: {len(namelist)} entries, 0 corrupted files.")
    else:
        print(f"[ERROR] Corrupted file found in archive: {test_result}")
