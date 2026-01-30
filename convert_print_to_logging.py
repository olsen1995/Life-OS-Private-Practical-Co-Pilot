import re
import logging  # ✅ Fix: needed so Pylance doesn't complain
from pathlib import Path

# Directories to skip
EXCLUDE_DIRS = {"venv", ".venv", "env", "__pycache__", "site-packages"}


def should_exclude(path: Path) -> bool:
    """Return True if file is inside excluded folders."""
    return any(part in EXCLUDE_DIRS for part in path.parts)


def convert_prints_in_file(filepath: Path):
    """Convert print(...) statements into logging.info(...)."""

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    modified = False
    new_lines = []

    # Check if logging is already imported
    logging_imported = any("import logging" in line for line in lines)

    for line in lines:
        stripped = line.strip()

        # Only match real print() calls at line start
        if re.match(r"^print\s*\(", stripped):
            indent_match = re.match(r"\s*", line)
            indent = indent_match.group(0) if indent_match else ""

            # Replace print(...) → logging.info(...)
            content = line.strip()[5:]  # removes "print"
            new_lines.append(f"{indent}logging.info{content}\n")
            modified = True
        else:
            new_lines.append(line)

    # Insert import logging if needed
    if modified and not logging_imported:
        insert_index = 0

        # Insert after existing imports
        for i, line in enumerate(new_lines):
            if line.startswith("import") or line.startswith("from"):
                insert_index = i + 1

        new_lines.insert(insert_index, "import logging\n")

    # Write file back if changes were made
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        logging.info(f"✅ Updated: {filepath}")
    else:
        logging.info(f"⏭️ No print() found: {filepath}")


def main():
    root = Path(".").resolve()
    logging.info("\n🔍 Scanning repo for print() statements...\n")

    for py_file in root.rglob("*.py"):
        if not should_exclude(py_file):
            convert_prints_in_file(py_file)

    logging.info("\n🎉 Done! All print() calls converted to logging.info().\n")


if __name__ == "__main__":
    main()
