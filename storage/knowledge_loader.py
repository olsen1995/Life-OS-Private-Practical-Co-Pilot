import os
import json
from typing import Dict, Any

class KnowledgeLoader:
    def __init__(self, folder: str = "knowledge"):
        self.folder = folder

    def load_all(self) -> Dict[str, Any]:
        knowledge = {}
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        for filename in os.listdir(self.folder):
            if filename.endswith(".json"):
                path = os.path.join(self.folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    knowledge[filename.replace(".json", "")] = data
        return knowledge
