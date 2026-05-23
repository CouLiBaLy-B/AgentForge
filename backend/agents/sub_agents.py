from agentforge.backend.tools.github_tools import github_clone_repo, execute_command
from agentforge.backend.tools.reviewer_tools import security_scan_python, analyze_complexity
from agentforge.backend.core.config import settings

coder_agent = {
    "name": "coder",
    "model": settings.CODER_MODEL,
    "description": "Expert software developer. Clones repos, writes code, and runs tests.",
    "system_prompt": """You are a senior developer expert. 
    You work inside a sandbox. 
    1. Clone the repo.
    2. Read files and plan.
    3. Use 'execute_command' for any shell action (pytest, git, etc).
    """,
    "tools": [github_clone_repo, execute_command],
    "skills_dir": f"{settings.SKILLS_DIR}/coder/",
}

reviewer_agent = {
    "name": "reviewer",
    "model": settings.REVIEWER_MODEL,
    "description": "Expert code reviewer.",
    "system_prompt": """Review code for security and quality. Use tools provided.""",
    "tools": [security_scan_python, analyze_complexity, execute_command],
    "skills_dir": f"{settings.SKILLS_DIR}/reviewer/",
}

pr_agent = {
    "name": "pr_creator",
    "model": settings.MAIN_MODEL,
    "description": "Git & GitHub expert.",
    "system_prompt": """Handle branches and commits using 'execute_command'.""",
    "tools": [execute_command],
    "skills_dir": f"{settings.SKILLS_DIR}/git/",
}
