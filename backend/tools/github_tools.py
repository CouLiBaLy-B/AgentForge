import requests
from langchain_core.tools import tool
from backend.core.sandbox import sandbox
from backend.core.config import settings

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
    repo_name = repo.split('/')[-1]
    url = f"https://x-access-token:{settings.GITHUB_TOKEN}@github.com/{repo}.git"
    
    cmd = f"git clone --branch {branch} --depth 50 {url} /workspace/{repo_name}"
    return_code, stdout, stderr = sandbox.execute(cmd)
    
    if return_code == 0:
        return f"Repo {repo} cloned successfully to /workspace/{repo_name}"
    return f"Failed to clone: {stderr}"

@tool
def create_pull_request(repo: str, branch: str, title: str, body: str) -> str:
    """Create a PR on GitHub. Requires valid branch and repo."""
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}", 
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"title": title, "body": body, "head": branch, "base": "main"}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        pr = response.json()
        return f"PR created successfully: {pr['html_url']}"
    return f"Error creating PR: {response.text}"
