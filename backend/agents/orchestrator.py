from deepagents import create_deep_agent
from agentforge.backend.agents.sub_agents import coder_agent, reviewer_agent, pr_agent
from agentforge.backend.tools.github_tools import create_pull_request
from agentforge.backend.tools.kanban_tools import kanban_update_status
from agentforge.backend.tools.slack_tools import slack_send_message
from agentforge.backend.core.config import settings
from agentforge.backend.core.memory_manager import memory_manager
from agentforge.backend.core.logger import agent_logger

def get_orchestrator(repo: str, task_id: str = "default"):
    repo_memory = memory_manager.get_repo_memory(repo)
    conventions_text = "\n".join([f"- {c}" for c in repo_memory.get("conventions", [])])
    
    # Custom tool to bridge orchestrator and internal logger
    from langchain_core.tools import tool
    @tool
    def log_task_event(event: str, details: str = ""):
        """Logs an important event for the current task."""
        agent_logger.log_event(task_id, "orchestrator", event, details)
        return "Event logged."

    return create_deep_agent(
        model="openai:deepseek-v4",
        model_kwargs={
            "base_url": settings.VLLM_BASE_URL,
            "temperature": 0.1,
        },
        system_prompt=f"""You are AgentForge Orchestrator.
        
        REPO CONTEXT: {conventions_text}
        
        LOGGING:
        Use `log_task_event` to record major milestones (e.g., 'Coder started', 'Review completed').
        
        Workflow:
        1. PLAN: `write_todos`.
        2. LOG: Start of task.
        3. DELEGATE: Coder -> Reviewer -> PR Agent.
        4. LOG: Final result.
        """,
        sub_agents=[coder_agent, reviewer_agent, pr_agent],
        tools=[create_pull_request, kanban_update_status, slack_send_message, log_task_event],
        skills_dir="./skills/orchestrator/",
        memory=[f"agentforge/backend/memory/{repo.replace('/', '_')}.md"],
        interrupt_on=["create_pull_request"],
    )
