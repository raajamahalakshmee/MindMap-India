#!/usr/bin/env python3
"""
Development Environment Setup Script for Mindmap India

This script helps set up the development environment with all necessary dependencies.
"""
import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Optional

def run_command(cmd: List[str], cwd: Optional[str] = None) -> bool:
    """Run a shell command and return True if successful."""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version() -> bool:
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"Current Python version: {platform.python_version()}")
        return False
    return True

def create_virtual_env(venv_path: Path) -> bool:
    """Create a Python virtual environment."""
    if venv_path.exists():
        print(f"Virtual environment already exists at {venv_path}")
        return True
    
    print(f"Creating virtual environment at {venv_path}")
    return run_command([sys.executable, "-m", "venv", str(venv_path)])

def install_dependencies(venv_path: Path) -> bool:
    """Install project dependencies using pip."""
    pip_cmd = [
        str(venv_path / "Scripts" / "pip") if os.name == 'nt' else str(venv_path / "bin" / "pip"),
        "install",
        "-r", "requirements.txt"
    ]
    
    # Also install development dependencies from notebooks/requirements.txt
    notebooks_req = Path("notebooks/requirements.txt")
    if notebooks_req.exists():
        pip_cmd.extend(["-r", str(notebooks_req)])
    
    return run_command(pip_cmd)

def setup_git_hooks() -> bool:
    """Set up Git hooks if not already set up."""
    git_dir = Path(".git")
    if not git_dir.exists():
        print("Not a Git repository. Skipping Git hooks setup.")
        return False
    
    hooks_dir = git_dir / "hooks"
    pre_commit = hooks_dir / "pre-commit"
    
    if not hooks_dir.exists():
        hooks_dir.mkdir()
    
    # Create a simple pre-commit hook that runs black and flake8
    if not pre_commit.exists():
        pre_commit_content = """#!/bin/sh
# Run black
black .

# Run flake8
flake8 .
"""
        try:
            with open(pre_commit, 'w', encoding='utf-8') as f:
                f.write(pre_commit_content)
            
            # Make the hook executable
            if os.name != 'nt':  # Skip on Windows
                os.chmod(pre_commit, 0o755)
            
            print("Created pre-commit hook for code formatting and linting.")
            return True
        except Exception as e:
            print(f"Error creating pre-commit hook: {e}")
            return False
    return True

def main() -> int:
    """Main function to set up the development environment."""
    print("=" * 50)
    print("Setting up Mindmap India development environment")
    print("=" * 50)
    print()
    
    if not check_python_version():
        return 1
    
    # Create necessary directories
    for dir_path in ["output", "output/wordclouds", "cache"]:
        Path(dir_path).mkdir(exist_ok=True)
    
    # Create and activate virtual environment
    venv_path = Path(".venv")
    if not create_virtual_env(venv_path):
        return 1
    
    # Install dependencies
    print("\nInstalling dependencies...")
    if not install_dependencies(venv_path):
        print("Error installing dependencies.")
        return 1
    
    # Set up Git hooks
    print("\nSetting up Git hooks...")
    setup_git_hooks()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nTo activate the virtual environment, run:")
    if os.name == 'nt':  # Windows
        print(f"  .\\{venv_path}\\Scripts\\activate")
    else:  # Unix/Linux/MacOS
        print(f"  source {venv_path}/bin/activate")
    print("\nTo run the application:")
    print("  python run.py")
    print("\nOr on Windows, you can simply run:")
    print("  .\\run_analysis.bat")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
