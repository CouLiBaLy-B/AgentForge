import os
import subprocess
from typing import List, Tuple
from agentforge.backend.core.config import settings

class Sandbox:
    """
    Handles code execution in an isolated environment.
    For production, this would use Modal, Daytona, or Runloop.
    For this implementation, we provide a local Docker-based sandbox.
    """
    def __init__(self, image_name: str = "agentforge-sandbox:latest"):
        self.image_name = image_name
        self.container_name = "agentforge_exec_env"

    def execute(self, command: str, cwd: str = "/workspace") -> Tuple[int, str, str]:
        """Executes a command inside the sandbox."""
        # Ensure the container is running
        self._ensure_container()
        
        full_command = ["docker", "exec", "-w", cwd, self.container_name, "bash", "-c", command]
        result = subprocess.run(full_command, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr

    def _ensure_container(self):
        """Checks if the container is running, starts it if not."""
        check = subprocess.run(["docker", "ps", "-q", "-f", f"name={self.container_name}"], capture_output=True)
        if not check.stdout:
            # Check if it exists but is stopped
            check_stopped = subprocess.run(["docker", "ps", "-aq", "-f", f"name={self.container_name}"], capture_output=True)
            if check_stopped.stdout:
                subprocess.run(["docker", "start", self.container_name])
            else:
                # Run a new one
                subprocess.run([
                    "docker", "run", "-d", "--name", self.container_name,
                    "-v", f"{os.path.abspath(settings.WORKSPACE_DIR)}:/workspace",
                    self.image_name, "tail", "-f", "/dev/null"
                ])

sandbox = Sandbox()
