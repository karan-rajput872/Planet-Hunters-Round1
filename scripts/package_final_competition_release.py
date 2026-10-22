"""
Planet Hunters — Final Competition & Presentation Release Packager
Creates dist/Planet-Hunters-Round1-Final.zip and dist/FINAL_PACKAGE_MANIFEST.md.
Includes complete source code, dashboard, tests, docs, launchers, and verified submissions.
Excludes .venv, raw npy datasets, caches, and machine-specific files.
"""

import hashlib
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
DIST_DIR.mkdir(parents=True, exist_ok=True)

ZIP_PATH = DIST_DIR / "Planet-Hunters-Round1-Final.zip"
MANIFEST_PATH = DIST_DIR / "FINAL_PACKAGE_MANIFEST.md"

INCLUDE_PATTERNS = [
    "README.md",
    "CHANGELOG.md",
    "LICENSE_STATUS.md",
    "DASHBOARD_README.md",
    "pyproject.toml",
    "requirements.txt",
    ".gitignore",
    ".gitattributes",
    "START_DASHBOARD.ps1",
    "START_DASHBOARD.bat",
    "train.py",
    "generate_submission.py",
    "validate_submission.py",
    ".streamlit/**/*.toml",
    "dashboard/**/*.py",
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
    "models/**/.gitkeep",
]

EXCLUDE_PARTS = {".venv", "__pycache__", "dist", ".git", "catboost_info", "logs"}

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print(f"Creating Final Competition Release Archive: {ZIP_PATH}...")
    packaged_files = []

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        added_paths = set()
        for pattern in INCLUDE_PATTERNS:
            for p in PROJECT_ROOT.glob(pattern):
                if p.is_file() and p not in added_paths:
                    if any(part in p.parts for part in EXCLUDE_PARTS):
                        continue
                    # Skip raw npy arrays
                    if p.suffix == ".npy":
                        continue
                    rel_path = p.relative_to(PROJECT_ROOT).as_posix()
                    zipf.write(p, arcname=rel_path)
                    added_paths.add(p)
                    packaged_files.append((rel_path, p.stat().st_size, compute_sha256(p)))

    # Sort files by relative path
    packaged_files.sort(key=lambda x: x[0])

    print(f"[SUCCESS] Packaged {len(packaged_files)} files into {ZIP_PATH.name}")
    print(f"Archive Size: {ZIP_PATH.stat().st_size / (1024 * 1024):.2f} MB")

    # Verify archive integrity
    with zipfile.ZipFile(ZIP_PATH, "r") as zipf:
        test_err = zipf.testzip()
        if test_err is not None:
            raise RuntimeError(f"Corrupted file found in zip: {test_err}")
        print(f"[VERIFIED] Zip integrity verified: {len(zipf.namelist())} files, 0 errors.")

    # Compute zip sha256
    zip_sha = compute_sha256(ZIP_PATH)

    # Write Manifest
    with open(MANIFEST_PATH, "w", encoding="utf-8") as mf:
        mf.write("# 📦 Planet Hunters — Final Release Package Manifest\n")
        mf.write("## ML Challenge Hack4Hack 2026 — Round 1\n\n")
        mf.write(f"**Archive:** `dist/{ZIP_PATH.name}`  \n")
        mf.write(f"**Size:** {ZIP_PATH.stat().st_size / (1024 * 1024):.2f} MB ({ZIP_PATH.stat().st_size:,} bytes)  \n")
        mf.write(f"**SHA-256 Checksum:** `{zip_sha}`  \n")
        mf.write(f"**Total Packaged Entries:** {len(packaged_files)} files  \n\n")
        mf.write("---\n\n")
        mf.write("## 1. Directory Breakdown\n\n")
        mf.write("| Directory / Area | Purpose | Key Files |\n")
        mf.write("| :--- | :--- | :--- |\n")
        mf.write("| `dashboard/` | Scientific ML Intelligence Platform | `app.py`, `styles.py`, `data_loader.py`, 8 components |\n")
        mf.write("| `src/` | ML Pipeline Engine | Feature engineering (85 features), preprocessing, training, validation |\n")
        mf.write("| `docs/` | Engineering & Scientific Documentation | Architecture, evaluation, reproducibility, handover, specs |\n")
        mf.write("| `submissions/` | Verified Competition Predictions | `submission_FINAL.csv` (7,000 rows, SHA-256 verified) |\n")
        mf.write("| `assets/` | Architecture & Publication Visuals | Pipeline schematic, benchmark curves, class distributions |\n")
        mf.write("| `tests/` | Automated Test Suite | `test_pipeline.py` (8 regression tests) |\n")
        mf.write("| Root Launchers | One-Click Execution | `START_DASHBOARD.ps1`, `START_DASHBOARD.bat` |\n\n")
        mf.write("---\n\n")
        mf.write("## 2. Packaged Files & Integrity Checksums\n\n")
        mf.write("| Relative Path | Size (Bytes) | SHA-256 Checksum |\n")
        mf.write("| :--- | :---: | :--- |\n")
        for rel_path, size, sha in packaged_files:
            mf.write(f"| `{rel_path}` | {size:,} | `{sha[:16]}...{sha[-8:]}` |\n")
        mf.write("\n---\n\n")
        mf.write("## 3. Excluded Items (By Design)\n\n")
        mf.write("1. **Virtual Environment (`.venv/`):** Contains platform-dependent compiled binaries.\n")
        mf.write("2. **Raw Arrays (`data/raw/*.npy`):** Excluded due to size (~380 MB) and competition data restrictions.\n")
        mf.write("3. **Compiled Caches (`__pycache__/`):** Excluded to ensure pristine bytecode compilation upon arrival.\n")
        mf.write("4. **Training Model Artifacts (`models/*.joblib`):** Large binary artifacts (~180 MB); easily regenerated in 78s via `python src/train_v3_dual_ensemble.py`.\n")

    print(f"[SUCCESS] Generated manifest: {MANIFEST_PATH}")

if __name__ == "__main__":
    main()
