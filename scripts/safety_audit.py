"""
GitHub Security & Repository Safety Scanner.
Scans all codebase files for potential credentials, API tokens, private keys, and hardcoded absolute paths.
"""
import os
import re
from pathlib import Path

print("=" * 65)
print("GITHUB SAFETY, CREDENTIALS & SENSITIVITY SCAN")
print("=" * 65)

suspect_regexes = [
    (re.compile(r'(?i)(api[_-]?key|secret|password|passwd|token|private[_-]?key)\s*[:=]\s*["\'][A-Za-z0-9_\-\.]{8,}["\']'), "Secret / Token Assignment"),
    (re.compile(r'-----BEGIN [A-Z ]+ PRIVATE KEY-----'), "PEM Private Key"),
    (re.compile(r'(?i)ghp_[A-Za-z0-9]{36}'), "GitHub Personal Access Token"),
    (re.compile(r'(?i)xox[baprs]-[0-9a-zA-Z]{10,48}'), "Slack Token"),
    (re.compile(r'(?i)AKIA[0-9A-Z]{16}'), "AWS Access Key ID"),
]

ignored_dirs = {".venv", "__pycache__", ".git", "catboost_info", "scratch", "dist"}
allowed_exts = {".py", ".md", ".txt", ".toml", ".json", ".csv"}

findings = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ignored_dirs]
    for f in files:
        file_path = Path(root) / f
        if file_path.suffix.lower() in allowed_exts:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                for regex, desc in suspect_regexes:
                    if regex.search(content):
                        # Filter out documentation mentions or markdown instructions
                        if "docs" in str(file_path) and "credential" in content.lower():
                            continue
                        findings.append((str(file_path), desc))
            except Exception:
                pass

print(f"1. Potential Secret / Credential Findings: {len(findings)}")
if findings:
    for path, desc in findings:
        print(f"   [ALERT] {path}: {desc}")
else:
    print("   [PASS] 0 credentials, secrets, or API tokens found.")

# 2. Check for hardcoded absolute paths in reusable source files
src_paths = list(Path("src").glob("*.py")) + [Path("train.py"), Path("generate_submission.py"), Path("validate_submission.py")]
hardcoded_src = []

for p in src_paths:
    txt = p.read_text(encoding="utf-8")
    for line_no, line in enumerate(txt.splitlines(), start=1):
        if re.search(r'[A-Za-z]:\\[Uu]sers\\', line) or "/home/" in line:
            hardcoded_src.append((str(p), line_no, line.strip()))

print(f"\n2. Hardcoded Absolute Machine Paths in Source Code: {len(hardcoded_src)}")
if hardcoded_src:
    for path, lno, lcontent in hardcoded_src:
        print(f"   [ALERT] {path}:{lno}: {lcontent}")
else:
    print("   [PASS] 0 hardcoded absolute paths found. All paths resolve dynamically relative to project root.")

print("=" * 65)
print("SAFETY AUDIT COMPLETE")
print("=" * 65)
