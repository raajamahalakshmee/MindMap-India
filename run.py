"""
Main entry point for the Mindmap India application.

This script initializes and runs the Streamlit web application.
"""
import os
import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def setup_logging():
    """Configure logging for the application."""
    log_dir = project_root / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def main():
    """Run the Streamlit application."""
    logger = setup_logging()
    
    try:
        import streamlit as st
        from mindmap.app import MindmapApp
        
        # Initialize and run the app
        app = MindmapApp()
        app.run()
        
    except ImportError as e:
        logger.error(f"Missing required dependencies: {e}")
        print(f"Error: {e}")
        print("Please install the required dependencies using:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.exception("An error occurred while running the application")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
