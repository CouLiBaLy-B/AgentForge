import asyncio
import os
import requests
from mcp.server.fastmcp import FastMCP
from backend.core.config import settings

# Initialize FastMCP Server
# This server acts as a plugin for Claude Code, giving it "Skills"
mcp = FastMCP("AgentForge Skills")

@mcp.tool()
async def update_kanban(task_id: str, status: str, message: str = "") -> str:
    """
    Updates the Kanban board status.
    Skills: [project-management, workflow]
    """
    url = f"{settings.KANBAN_API_URL}/api/tasks/{task_id}"
    try:
        response = requests.patch(url, json={"status": status, "message": message})
        return f"Kanban updated to {status}"
    except Exception as e:
        return f"Failed to update Kanban: {str(e)}"

@mcp.tool()
async def notify_slack(text: str, channel: str = None) -> str:
    """
    Sends a notification to the development Slack channel.
    Skills: [communication, alerts]
    """
    token = settings.SLACK_BOT_TOKEN
    target_channel = channel or "dev-notifications"
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        requests.post(url, headers=headers, json={"channel": target_channel, "text": text})
        return "Slack notification sent."
    except Exception as e:
        return f"Slack failed: {str(e)}"

@mcp.tool()
async def run_security_scan(repo_path: str = "/workspace") -> str:
    """
    Performs a Bandit security scan on the provided path.
    Skills: [security, auditing]
    """
    import subprocess
    result = subprocess.run(["bandit", "-r", repo_path, "-f", "txt"], capture_output=True, text=True)
    return result.stdout if result.stdout else "No security issues found."

if __name__ == "__main__":
    mcp.run()
