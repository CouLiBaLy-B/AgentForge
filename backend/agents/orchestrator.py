from deepagents import create_deep_agent
from deepagents.middleware import (
    SubAgentMiddleware,
    FilesystemMiddleware,
    TodoListMiddleware,
    SummarizationMiddleware,
    SkillsMiddleware,
    MemoryMiddleware
)
from agentforge.backend.agents.sub_agents import coder_agent, reviewer_agent, pr_agent
from agentforge.backend.tools.github_tools import create_pull_request
from agentforge.backend.tools.kanban_tools import kanban_update_status
from agentforge.backend.tools.slack_tools import slack_send_message
from agentforge.backend.core.config import settings
from agentforge.backend.core.memory_manager import memory_manager
from agentforge.backend.core.logger import agent_logger
from langchain_core.tools import tool

def get_orchestrator(repo: str, task_id: str = "default"):
    repo_memory = memory_manager.get_repo_memory(repo)
    conventions_text = "\n".join([f"- {c}" for c in repo_memory.get("conventions", [])])
    
    @tool
    def log_task_event(event: str, details: str = ""):
        """Logs an important event for the current task."""
        agent_logger.log_event(task_id, "orchestrator", event, details)
        return "Event logged."

    # Define the middleware stack explicitly
    middleware = [
        TodoListMiddleware(),  # Handles planning with write_todos
        FilesystemMiddleware(root_dir=settings.WORKSPACE_DIR), # Safe file access
        SkillsMiddleware(skills_dir=settings.SKILLS_DIR), # Progressive disclosure
        SubAgentMiddleware(), # Orchestrates coder/reviewer/pr agents
        SummarizationMiddleware(token_limit=32000), # Auto-summarize long contexts
        MemoryMiddleware() # Handles AGENTS.md and memory injection
    ]

    return create_deep_agent(
        model=settings.MAIN_MODEL,
        model_kwargs={
            "base_url": settings.VLLM_BASE_URL,
            "temperature": settings.TEMPERATURE,
        },
        system_prompt=f"""You are AgentForge Orchestrator.
        
        REPO CONTEXT: {conventions_text}
        
        WORKFLOW:
        1. PLAN: You MUST use `write_todos` to create a plan before starting.
        2. LOG: Record milestones via `log_task_event`.
        3. DELEGATE: Use the `task` tool to call specialized sub-agents.
        4. APPROVAL: Wait for HITL before `create_pull_request`.
        """,
        sub_agents=[coder_agent, reviewer_agent, pr_agent],
        tools=[create_pull_request, kanban_update_status, slack_send_message, log_task_event],
        middleware=middleware, # Explicitly passing the middleware stack
        interrupt_on=["create_pull_request"],
    )
