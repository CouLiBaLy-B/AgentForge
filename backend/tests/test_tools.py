import pytest
from unittest.mock import patch, MagicMock
from backend.tools.github_tools import github_clone_repo
from backend.core.memory_manager import MemoryManager

def test_memory_manager_conventions():
    # Use a local path that exists in the CI environment
    mm = MemoryManager(storage_dir="./backend/tests/memory_tmp")
    repo = "test/repo"
    mm.add_convention(repo, "Standard indent: 4 spaces")
    
    mem = mm.get_repo_memory(repo)
    assert "Standard indent: 4 spaces" in mem["conventions"]
    
    # Cleanup
    import shutil
    import os
    if os.path.exists("./backend/tests/memory_tmp"):
        shutil.rmtree("./backend/tests/memory_tmp")

@patch("backend.core.sandbox.sandbox.execute")
def test_github_clone_tool(mock_execute):
    mock_execute.return_value = (0, "Cloned", "")
    res = github_clone_repo.invoke({"repo": "org/repo", "branch": "main"})
    assert "cloned successfully" in res
    mock_execute.assert_called_once()
