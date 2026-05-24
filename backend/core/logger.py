import json
import os
from datetime import datetime
from pathlib import Path
from backend.core.config import settings

class AgentLogger:
    def __init__(self, logs_dir: str = None):
        self.logs_dir = Path(logs_dir or settings.LOGS_DIR)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_path(self, task_id: str) -> Path:
        return self.logs_dir / f"{task_id}.json"

    def log_event(self, task_id: str, agent_name: str, event: str, details: str = ""):
        path = self._get_log_path(task_id)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent_name,
            "event": event,
            "details": details
        }
        
        logs = []
        if path.exists():
            with open(path, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        
        logs.append(log_entry)
        with open(path, "w") as f:
            json.dump(logs, f, indent=2)

    def get_logs(self, task_id: str):
        path = self._get_log_path(task_id)
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
        return []

agent_logger = AgentLogger()
