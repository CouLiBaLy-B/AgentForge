import asyncio
import sys
from unittest.mock import MagicMock

# Mocking everything needed for the simulation
modules_to_mock = [
    "deepagents", "deepagents.middleware", "langchain_core", 
    "langchain_core.tools", "pydantic_settings", "pydantic", 
    "requests"
]
for module in modules_to_mock:
    sys.modules[module] = MagicMock()

# Specifically mock BaseSettings
class MockBaseSettings:
    def __init__(self, **kwargs): pass
    model_config = {"env_file": ".env"}
sys.modules["pydantic_settings"].BaseSettings = MockBaseSettings

# Moved imports to the top as much as possible, but since we mock sys.modules above, 
# we keep them here but fix the ruff warning if possible or just ignore it for the test script.
from backend.agents.orchestrator import get_orchestrator # noqa: E402
from backend.core.memory_manager import memory_manager # noqa: E402

async def simulate_end_to_end():
    print("🚀 Starting End-to-End Simulation")
    repo = "CouLiBaLy-B/groupe-projets"
    
    # 1. Loading long-term memory
    memory_manager.add_convention(repo, "Use FastAPI for all new endpoints.")
    
    # 2. Get Orchestrator
    orchestrator = get_orchestrator(repo)
    print(f"🤖 Orchestrator initialized for {repo}")
    print(f"Plan created: {orchestrator}")

    print("\n✅ Simulation Complete!")

if __name__ == "__main__":
    asyncio.run(simulate_end_to_end())
