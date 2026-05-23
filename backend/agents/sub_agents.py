from agentforge.backend.tools.github_tools import github_clone_repo
from agentforge.backend.tools.reviewer_tools import security_scan_python, analyze_complexity

coder_agent = {
    "name": "coder",
    "description": "Expert software developer. Clones repos, writes code, and runs tests.",
    "system_prompt": """You are a senior developer expert. 
    Workflow:
    1. Clone/Explore.
    2. Plan (write_todos).
    3. Implement.
    4. Test.
    """,
    "tools": [github_clone_repo],
    "skills_dir": "./skills/coder/",
}

reviewer_agent = {
    "name": "reviewer",
    "description": "Expert code reviewer. Analyzes quality, security, and performance.",
    "system_prompt": """You are a senior code reviewer. 
    Analyze the implementation. 
    Mandatory steps:
    1. Run `security_scan_python` to check for vulnerabilities.
    2. Check complexity using `analyze_complexity`.
    3. Verify logic and readability.
    Produce a report in REVIEW.md.
    """,
    "tools": [security_scan_python, analyze_complexity],
    "skills_dir": "./skills/reviewer/",
}

pr_agent = {
    "name": "pr_creator",
    "description": "Git & GitHub expert. Handles branching, commits, and PR creation.",
    "system_prompt": """You are a Git expert.""",
    "tools": [],
    "skills_dir": "./skills/git/",
}
