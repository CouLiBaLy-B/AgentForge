# 📖 AgentForge Documentation

This guide provides deep technical insights into the AgentForge ecosystem.

## 1. The Orchestration Logic
The `orchestrator.py` uses the `create_deep_agent` factory. It is configured with:
- **TodoListMiddleware**: Forces the agent to think before acting.
- **FilesystemMiddleware**: Restricts the agent to a sandboxed `/workspace` directory.
- **SubAgentMiddleware**: Manages the life cycle of specialized sub-agents.

## 2. Long-Term Memory
Memory is stored in `backend/memory/`. When a task starts, the system:
1. Loads the JSON file associated with the repo.
2. Injects conventions into the Orchestrator's system prompt.
3. Updates the JSON file with "Learned Lessons" after the task completes.

## 3. Sub-Agent Workflows

### 💻 Coder Agent
- **Tools**: `github_clone_repo`, `write_file`, `edit_file`, `execute`.
- **Goal**: Implement the requested feature and ensure tests pass.

### 🔍 Reviewer Agent
- **Tools**: `security_scan_python`, `analyze_complexity`.
- **Goal**: Act as a gatekeeper. It must generate a `REVIEW.md` in the workspace.

### 📋 PR Agent
- **Tools**: `create_pull_request`, `git_push`.
- **Goal**: Finalize the Git flow. Triggered only after user approval (HITL).

## 4. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks` | Create a new dev task |
| POST | `/api/tasks/{id}/start` | Trigger the AI Agent |
| GET | `/api/tasks/{id}/logs` | Fetch real-time agent logs |
| POST | `/api/slack/commands` | Handle Slack commands |

## 5. Security & Isolation
In production, every task runs in a **Modal Sandbox** or a fresh Docker container. This ensures that the agent cannot execute malicious commands on the host system.
