import sys
from pathlib import Path

EXCLUDE_DIRS = {"venv", ".venv", "env", "__pycache__", "site-packages"}

def should_exclude(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)

def main():
    root = Path(".").resolve()
    bad_files = []

    for py_file in root.rglob("*.py"):
        if should_exclude(py_file):
            continue

        content = py_file.read_text(encoding="utf-8")

        if "print(" in content:
            bad_files.append(py_file)

    if bad_files:
        print("\n🚨 COMMIT BLOCKED — print() detected!\n")
        for f in bad_files:
            print(f"❌ {f}")

        print("\n✅ Replace print() with logging.info() before committing.\n")
        sys.exit(1)

    print("✅ No print() statements found. Commit allowed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
