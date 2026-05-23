# 🏗️ AgentForge: Agentic AI Developer Platform

AgentForge is a state-of-the-art autonomous development platform designed to handle software engineering tasks from end-to-end. Powered by **LangChain DeepAgents (v0.5, 2026)** and **vLLM**, it orchestrates specialized agents to code, review, and manage Pull Requests directly from Slack or a dedicated Kanban board.

---

## 🌟 Key Features

- **Autonomous Orchestration**: Uses a "Main Agent" to decompose complex tasks into sub-tasks delegated to specialized Coder, Reviewer, and Git agents.
- **Long-Term Memory**: Remembers repository-specific coding conventions, past issues, and learned patterns across different tasks.
- **Human-in-the-Loop (HITL)**: Mandatory approval steps for critical actions like pushing code or creating Pull Requests.
- **Real-Time Kanban Board**: A React-based dashboard to visualize agent progress, view logs, and manage the task backlog via WebSockets.
- **Slack Integration**: Command your AI dev team via `/task` and `/ask` slash commands.
- **Security First**: Integrated security scanning using `Bandit` and complexity analysis before any code is approved.

---

## 🏛️ Architecture

```text
┌────────────────┐      ┌───────────────────┐      ┌────────────────┐
│   Slack / UI   │ ───▶ │  FastAPI Gateway  │ ───▶ │  Orchestrator  │
└────────────────┘      └─────────┬─────────┘      └───────┬────────┘
                                  │                        │
                    ┌─────────────┴─────────────┐   ┌──────┴──────┐
                    │  Postgres (Memory/State)  │   │ vLLM Server │
                    └───────────────────────────┘   └─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │  DeepAgents Stack         │
                    │ (Coder, Reviewer, PR)     │
                    └───────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- A GitHub Personal Access Token (PAT)
- Slack Bot Token (optional, for Slack integration)
- An OpenAI-compatible LLM provider (vLLM, Ollama, or OpenAI)

### 1. Setup Environment
Create a `.env` file in the root directory:
```env
GITHUB_TOKEN=your_github_token
SLACK_BOT_TOKEN=your_slack_token
SLACK_SIGNING_SECRET=your_slack_secret
VLLM_BASE_URL=http://vllm:8000/v1
```

### 2. Launch with Docker
```bash
docker-compose up --build
```

Access the Kanban board at `http://localhost:80` and the API at `http://localhost:3000`.

---

## 🛠️ Tech Stack

- **Framework**: [LangChain DeepAgents](https://github.com/langchain-ai/deepagents)
- **Inference Engine**: [vLLM](https://github.com/vllm-project/vllm) (Model: DeepSeek-V4)
- **Backend**: FastAPI, WebSockets, SQLAlchemy
- **Frontend**: React, Tailwind CSS, Lucide Icons
- **Sandboxing**: Modal / Local Docker Isolation
- **Observability**: LangSmith Integration

---

## 📚 Agent Skills

AgentForge uses a **Progressive Disclosure** skill system. Instructions are loaded only when relevant to the task:
- `skills/coder/python_dev.md`: Best practices for Python, FastAPI, and Testing.
- `skills/reviewer/checklist.md`: Quality, security, and performance standards.
- `skills/git/workflow.md`: Branching strategy and PR templates.

---

## 🤝 Contributing
1. Create a task in the Kanban.
2. Let the AgentForge agent implement it.
3. Review the generated PR!

---

## 📄 License
MIT License. Created by Arena Agent for CouLiBaLy-B.
