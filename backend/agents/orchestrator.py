from deepagents import create_deep_agent
from deepagents.middleware import (
    SubAgentMiddleware,
    FilesystemMiddleware,
    SummarizationMiddleware,
    SkillsMiddleware,
    MemoryMiddleware
)
from backend.agents.sub_agents import coder_agent, reviewer_agent, pr_agent
from backend.tools.github_tools import create_pull_request
from backend.tools.kanban_tools import kanban_update_status
from backend.tools.slack_tools import slack_send_message
from backend.core.config import settings
from backend.core.memory_manager import memory_manager
from backend.core.logger import agent_logger
from langchain_core.tools import tool

def get_orchestrator(repo: str, task_id: str = "default"):
    repo_memory = memory_manager.get_repo_memory(repo)
    conventions_text = "\n".join([f"- {c}" for c in repo_memory.get("conventions", [])])
    
    @tool
    def log_task_event(event: str, details: str = ""):
        """Logs an important event for the current task."""
        agent_logger.log_event(task_id, "orchestrator", event, details)
        return "Event logged."

    base_url = settings.VLLM_BASE_URL if settings.LLM_SOURCE == "vllm" else settings.FREELLM_BASE_URL
    api_key = "no-key" if settings.LLM_SOURCE == "vllm" else settings.FREELLM_API_KEY

    # TodoListMiddleware removed as it is not present in the current deepagents version
    middleware = [
        FilesystemMiddleware(root_dir=settings.WORKSPACE_DIR),
        SkillsMiddleware(skills_dir=settings.SKILLS_DIR),
        SubAgentMiddleware(),
        SummarizationMiddleware(token_limit=32000),
        MemoryMiddleware()
    ]

    return create_deep_agent(
        model=settings.MAIN_MODEL,
        model_kwargs={
            "base_url": base_url,
            "api_key": api_key,
            "temperature": settings.TEMPERATURE,
        },
        system_prompt=f"""You are AgentForge Orchestrator.
        
        REPO CONTEXT: {conventions_text}
        
        WORKFLOW:
        1. PLAN: Organize your thoughts before starting.
        2. LOG: Start of task via log_task_event.
        3. DELEGATE: Use sub-agents (coder, reviewer, pr_creator) for specialized work.
        4. APPROVAL: Wait for human approval before final PR creation.
        """,
        sub_agents=[coder_agent, reviewer_agent, pr_agent],
        tools=[create_pull_request, kanban_update_status, slack_send_message, log_task_event],
        middleware=middleware,
        interrupt_on=["create_pull_request"],
    )
