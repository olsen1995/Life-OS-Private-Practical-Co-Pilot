import ast
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = REPO_ROOT / "lifeos"

# Define modules now under lifeos/
MOVED_MODULES = {
    "auth", "auth_manager", "scheduler", "mode_router", "api_key_mode",
    "memory_mode", "feedback_mode", "system_mode", "multi_mode", "notes_mode",
    "prompt_mode", "response_formatter", "debug_mode", "logger",
    "modes", "routes", "storage", "tools", "canon"
}

def rewrite_imports_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"⚠️ Skipping (syntax error): {file_path}")
        return

    new_lines = []
    modified = False

    for line in source.splitlines():
        stripped = line.strip()
        # Skip comments and empty lines
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue

        # Rewrite: from X import Y
        if stripped.startswith("from "):
            parts = stripped.split()
            if len(parts) > 1:
                mod = parts[1].split('.')[0]
                if mod in MOVED_MODULES and not parts[1].startswith("lifeos."):
                    line = line.replace(f"from {mod}", f"from lifeos.{mod}")
                    modified = True

        # Rewrite: import X
        elif stripped.startswith("import "):
            parts = stripped.split()
            if len(parts) > 1:
                mod = parts[1].split('.')[0]
                if mod in MOVED_MODULES and not parts[1].startswith("lifeos."):
                    line = line.replace(f"import {mod}", f"import lifeos.{mod}")
                    modified = True

        new_lines.append(line)

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        print(f"✅ Fixed: {file_path.relative_to(REPO_ROOT)}")


def scan_and_rewrite_imports():
    print("🔍 Scanning for imports to fix...\n")
    for path in REPO_ROOT.rglob("*.py"):
        if ".venv" in str(path):
            continue
        rewrite_imports_in_file(path)
    print("\n🎉 Done! All imports updated.")


if __name__ == "__main__":
    scan_and_rewrite_imports()
