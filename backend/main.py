import asyncio
import re
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

from agentforge.backend.agents.orchestrator import get_orchestrator
from agentforge.backend.core.config import settings
from agentforge.backend.core.security import verify_slack_signature
from agentforge.backend.core.logger import agent_logger

app = FastAPI(title="AgentForge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_tasks = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.post("/api/tasks")
async def create_task(title: str, repo: str, description: str = ""):
    task_id = str(uuid.uuid4())[:8]
    task = {
        "id": task_id,
        "title": title,
        "repo": repo,
        "status": "backlog",
        "description": description,
        "created_at": datetime.utcnow().isoformat()
    }
    db_tasks[task_id] = task
    await manager.broadcast({"type": "task_created", "task": task})
    return task

@app.get("/api/tasks/{task_id}/logs")
async def get_task_logs(task_id: str):
    return {"logs": agent_logger.get_logs(task_id)}

@app.post("/api/tasks/{task_id}/start")
async def start_agent(task_id: str):
    if task_id not in db_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task = db_tasks[task_id]
    task["status"] = "in_progress"
    await manager.broadcast({"type": "task_updated", "task": task})
    asyncio.create_task(run_orchestrator(task))
    return {"message": "Agent started"}

async def run_orchestrator(task: dict, slack_channel: str = None):
    # Pass task_id for logging
    orchestrator = get_orchestrator(task['repo'], task['id'])
    try:
        agent_logger.log_event(task['id'], "system", "Agent initialized", f"Processing {task['title']}")
        content = f"Execute task: {task['title']} for repo: {task['repo']}."
        await orchestrator.ainvoke({
            "messages": [{"role": "user", "content": content}]
        })
    except Exception as e:
        agent_logger.log_event(task['id'], "system", "Agent failed", str(e))
        if task["id"] in db_tasks:
            db_tasks[task["id"]]["status"] = "failed"
            await manager.broadcast({"type": "task_updated", "task": db_tasks[task["id"]]})

# ... Slack Handlers remain same ...

@app.websocket("/ws/board")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
