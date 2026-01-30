import os
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

# === Define Destination Layout === #
NEW_LAYOUT = {
    "core_modules": REPO_ROOT / "lifeos",
    "scripts_devtools": REPO_ROOT / "scripts/devtools",
    "scripts_logging": REPO_ROOT / "scripts/logging",
    "scripts_hooks": REPO_ROOT / "scripts/hooks",
    "logs_horoscope": REPO_ROOT / "logs/horoscope",
    "storage_data": REPO_ROOT / "storage/data",
    "docs_safety": REPO_ROOT / "docs/safety",
    "docs_automation": REPO_ROOT / "docs/automation",
    "docs_releases": REPO_ROOT / "docs/releases",
}

# === Create Target Folders === #
for name, path in NEW_LAYOUT.items():
    path.mkdir(parents=True, exist_ok=True)

# === Moves: Python App Files → lifeos/ === #
core_files = [
    "main.py", "auth.py", "auth_manager.py", "scheduler.py", "mode_router.py",
    "api_key_mode.py", "memory_mode.py", "feedback_mode.py", "system_mode.py",
    "multi_mode.py", "notes_mode.py", "prompt_mode.py", "response_formatter.py",
    "debug_mode.py", "logger.py"
]

for file in core_files:
    src = REPO_ROOT / file
    dst = NEW_LAYOUT["core_modules"] / file
    if src.exists():
        shutil.move(str(src), str(dst))

# === Moves: Whole Folders === #
move_dirs = {
    "routes": "core_modules",
    "modes": "core_modules",
    "storage": "core_modules",
    "tools": "core_modules",
    "canon": "core_modules",
    "scripts/devtools": "scripts_devtools",
    "scripts/logging": "scripts_logging",
    "scripts/hooks": "scripts_hooks",
    "daily-horoscope-log": "logs_horoscope",
    "data": "storage_data",
    "docs/safety": "docs_safety",
    "docs/automation": "docs_automation",
    "docs/releases": "docs_releases"
}

for src_dir, dest_key in move_dirs.items():
    src = REPO_ROOT / src_dir
    dst_base = NEW_LAYOUT[dest_key]
    dst = dst_base / Path(src).name

    # ❗ Prevent self-move (e.g., scripts/logging into scripts/logging/logging)
    if src.resolve() == dst.resolve() or dst.resolve().is_relative_to(src.resolve()):
        print(f"⏭️ Skipping self-move: {src}")
        continue

    if src.exists():
        shutil.move(str(src), str(dst))

# === Move loose horoscope .md file === #
for file in REPO_ROOT.glob("*.md"):
    if "horoscope" in file.stem.lower():
        shutil.move(str(file), str(NEW_LAYOUT["logs_horoscope"] / file.name))

print("\n✅ Refactor completed. Layout normalized. Review changes before committing.")
