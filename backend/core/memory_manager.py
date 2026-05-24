import json
import os
from pathlib import Path
from typing import Dict, Any
from agentforge.backend.core.config import settings

class MemoryManager:
    """
    Manages long-term persistence for repo-specific conventions and agent memories.
    Uses local JSON files in the demo, but would use Postgres MemoryStore in production.
    """
    def __init__(self, storage_dir: str = None):
        self.storage_dir = Path(storage_dir or settings.MEMORY_DIR)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, repo: str) -> Path:
        # Sanitize repo name for filename
        safe_name = repo.replace("/", "_").replace("\\", "_")
        return self.storage_dir / f"{safe_name}.json"

    def get_repo_memory(self, repo: str) -> Dict[str, Any]:
        path = self._get_path(repo)
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
        return {"conventions": [], "past_issues": [], "learned_skills": []}

    def save_repo_memory(self, repo: str, data: Dict[str, Any]):
        path = self._get_path(repo)
        existing = self.get_repo_memory(repo)
        existing.update(data)
        with open(path, "w") as f:
            json.dump(existing, f, indent=2)

    def add_convention(self, repo: str, convention: str):
        memory = self.get_repo_memory(repo)
        if convention not in memory["conventions"]:
            memory["conventions"].append(convention)
            self.save_repo_memory(repo, memory)

memory_manager = MemoryManager()
