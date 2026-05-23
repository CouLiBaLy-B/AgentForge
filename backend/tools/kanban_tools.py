import requests
from langchain_core.tools import tool
from agentforge.backend.core.config import settings

@tool
def kanban_update_status(task_id: str, status: str, message: str = "") -> str:
    """
    Updates the status of a task in the Kanban board.
    Status can be: backlog, todo, in_progress, review, done, failed.
    """
    url = f"{settings.KANBAN_API_URL}/api/tasks/{task_id}"
    data = {"status": status, "message": message}
    try:
        response = requests.patch(url, json=data)
        if response.status_code == 200:
            return f"Task {task_id} updated to {status}."
        return f"Failed to update task: {response.status_code} {response.text}"
    except Exception as e:
        return f"Connection error: {str(e)}"
