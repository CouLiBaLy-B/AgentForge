import os
from langchain_core.tools import tool
from backend.core.sandbox import sandbox

@tool
def execute_command(command: str, workdir: str = "/workspace") -> str:
    """
    Executes a shell command inside the isolated sandbox.
    Use this for git, pytest, pip install, etc.
    """
    return_code, stdout, stderr = sandbox.execute(command, cwd=workdir)
    if return_code == 0:
        return f"STDOUT:\n{stdout}"
    return f"ERROR (Exit Code {return_code}):\n{stderr}\nSTDOUT:\n{stdout}"

@tool
def github_clone_repo(repo: str, branch: str = "main") -> str:
    """Clone a GitHub repo into the sandbox workspace."""
    from backend.core.config import settings
    
    repo_name = repo.split('/')[-1]
    url = f"https://x-access-token:{settings.GITHUB_TOKEN}@github.com/{repo}.git"
    
    # Use the execute_command tool logic via sandbox
    cmd = f"git clone --branch {branch} --depth 50 {url} /workspace/{repo_name}"
    return_code, stdout, stderr = sandbox.execute(cmd)
    
    if return_code == 0:
        return f"Repo {repo} cloned successfully to /workspace/{repo_name}"
    return f"Failed to clone: {stderr}"
