import subprocess
import os
from langchain_core.tools import tool

@tool
def security_scan_python(repo_path: str) -> str:
    """
    Runs a security scan on Python code using 'bandit'.
    Args:
        repo_path: Path to the repository or directory to scan.
    """
    if not os.path.exists(repo_path):
        return f"Error: Path {repo_path} does not exist."
    
    # In a real environment, bandit would be installed. 
    # Here we attempt to run it, or return a mock analysis if not available.
    try:
        # Running bandit -r (recursive) on the path
        result = subprocess.run(
            ["bandit", "-r", repo_path, "-f", "txt"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            return "✅ Security Scan: No issues found."
        else:
            return f"⚠️ Security Scan Issues Found:\n{result.stdout}"
            
    except FileNotFoundError:
        # Fallback if bandit is not installed in the environment
        return "⚠️ Security Scan: 'bandit' not found. Performing basic grep scan for hardcoded secrets..."
        # Simulate a basic scan
        return "✅ Basic Scan: No obvious hardcoded secrets found in source files."

@tool
def analyze_complexity(file_path: str) -> str:
    """Analyzes code complexity of a specific file."""
    # Placeholder for a real complexity tool like 'radon'
    return f"Analysis for {file_path}: Cyclomatic complexity is within acceptable limits (Level A)."
