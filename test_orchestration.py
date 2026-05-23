import asyncio
import sys
from unittest.mock import MagicMock

# Mocking everything needed for the simulation
modules_to_mock = [
    "deepagents", "deepagents.middleware", "langchain_core", 
    "langchain_core.tools", "pydantic_settings", "pydantic", 
    "requests", "pydantic_settings"
]
for module in modules_to_mock:
    sys.modules[module] = MagicMock()

# Specifically mock BaseSettings to avoid inheritance errors
class MockBaseSettings:
    def __init__(self, **kwargs): pass
    class Config: env_file = ".env"
sys.modules["pydantic_settings"].BaseSettings = MockBaseSettings

from agentforge.backend.agents.orchestrator import get_orchestrator
from agentforge.backend.core.memory_manager import memory_manager

async def simulate_end_to_end():
    print("🚀 Starting End-to-End Simulation: 'Add Health Check to API'")
    
    repo = "CouLiBaLy-B/groupe-projets"
    
    # 1. Pre-task: Add a known convention to memory
    print("📝 Step 1: Loading long-term memory...")
    memory_manager.add_convention(repo, "Use FastAPI for all new endpoints.")
    memory_manager.add_convention(repo, "All endpoints must return JSON.")
    
    # 2. Get Orchestrator
    orchestrator = get_orchestrator(repo)
    print(f"🤖 Step 2: Orchestrator initialized for {repo}")
    
    # 3. Simulation of Agent logic
    print("🧠 Step 3: Orchestrator is planning (via TodoListMiddleware)...")
    print("   > [TODO] Clone repo")
    print("   > [TODO] Read src/app.py")
    print("   > [TODO] Delegate to 'coder' to add /health")
    
    print("🔧 Step 4: Coder Agent in action (using Skills/python_dev)...")
    print("   [coder] Modifying src/app.py...")
    
    print("🔍 Step 5: Reviewer Agent in action...")
    print("   [reviewer] Checking security and quality standards...")
    
    print("⚠️ Step 6: PR Creation (HITL Triggered via interrupt_on=['create_pull_request'])")
    print("   [orchestrator] Waiting for user approval on Slack...")
    print("   [USER] Approved! ✅")
    
    print("📦 Step 7: Finalizing PR...")
    print("   [pr_agent] Created PR #1: https://github.com/CouLiBaLy-B/groupe-projets/pull/1")
    
    # 4. Post-task: Save a new learned convention
    print("💾 Step 8: Updating Long-term memory with learned patterns...")
    memory_manager.add_convention(repo, "Project uses Pydantic for response models.")
    
    final_memory = memory_manager.get_repo_memory(repo)
    print("\n✅ Simulation Complete!")
    print(f"Current Memory for {repo}:")
    for convention in final_memory['conventions']:
        print(f"  - {convention}")

if __name__ == "__main__":
    asyncio.run(simulate_end_to_end())
