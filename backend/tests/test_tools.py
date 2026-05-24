import pytest
from unittest.mock import patch, MagicMock
from backend.tools.github_tools import github_clone_repo
from backend.core.memory_manager import MemoryManager

def test_memory_manager_conventions():
    mm = MemoryManager(storage_dir="agentforge/backend/tests/memory_tmp")
    repo = "test/repo"
    mm.add_convention(repo, "Standard indent: 4 spaces")
    
    mem = mm.get_repo_memory(repo)
    assert "Standard indent: 4 spaces" in mem["conventions"]
    
    # Cleanup
    import shutil
    shutil.rmtree("agentforge/backend/tests/memory_tmp")

@patch("agentforge.backend.core.sandbox.sandbox.execute")
def test_github_clone_tool(mock_execute):
    mock_execute.return_value = (0, "Cloned", "")
    res = github_clone_repo.invoke({"repo": "org/repo", "branch": "main"})
    assert "cloned successfully" in res
    mock_execute.assert_called_once()
