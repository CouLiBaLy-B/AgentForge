import requests
import subprocess
import os
from langchain_core.tools import tool
from agentforge.backend.core.config import settings

@tool
def github_clone_repo(repo: str, branch: str = "main") -> str:
    """Clone a GitHub repo into the workspace. Format: 'org/repo'"""
    repo_path = f"/home/user/agentforge/workspace/{repo.split('/')[-1]}"
    if os.path.exists(repo_path):
        return f"Repo already exists at {repo_path}"
    
    # Using HTTPS with token
    url = f"https://x-access-token:{settings.GITHUB_TOKEN}@github.com/{repo}.git"
    result = subprocess.run(
        ["git", "clone", "--branch", branch, "--depth", "50", url, repo_path],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return f"Repo {repo} cloned successfully to {repo_path}."
    return f"Failed to clone: {result.stderr}"

@tool
def create_pull_request(repo: str, branch: str, title: str, body: str) -> str:
    """Create a PR on GitHub. Requires valid branch and repo."""
    url = f"https://api.github.com/repos/{repo}/pulls"
    headers = {"Authorization": f"token {settings.GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {"title": title, "body": body, "head": branch, "base": "main"}
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        pr = response.json()
        return f"PR created successfully: {pr['html_url']}"
    return f"Error creating PR: {response.text}"
