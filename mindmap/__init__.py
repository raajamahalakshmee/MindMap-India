"""Mindmap India - AI-powered career exploration and recommendation system."""

__version__ = "1.0.0"
__author__ = "Mindmap India Team"
__email__ = "contact@mindmapindia.example.com"

# Import key components to make them available at the package level
from .utils import *  # noqa: F403
from .clustering import *  # noqa: F403
from .visualization import *  # noqa: F403

# Set up logging
import logging
from config import LOGGING_CONFIG
import logging.config

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Clean up the namespace
__all__ = [
    '__version__',
    '__author__',
    '__email__',
    'logger',
]
