import json
from pathlib import Path
from typing import Dict, Any

class KnowledgeLoader:
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)

    def load_all(self) -> Dict[str, Any]:
        data = {}
        for file in self.plugins_dir.glob("*.*"):
            if file.suffix.lower() == ".json":
                with open(file, "r", encoding="utf-8") as f:
                    data[file.stem] = json.load(f)
            else:
                data[file.stem] = str(file.resolve())
        return data
