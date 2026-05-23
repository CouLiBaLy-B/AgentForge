import { slack_notify_tool } from "../tools/slack_tools" # Hypothetical

# Skills setup
# ... same as before but adding slack notify to orchestrator

# The PR Agent specific skill
---
name: git_workflow
description: "Handles branches, commits and PRs"
---
1. git checkout -b feature/task-{id}
2. git add .
3. git commit -m "feat: {description}"
4. git push origin feature/task-{id}
5. create_pull_request(...)
