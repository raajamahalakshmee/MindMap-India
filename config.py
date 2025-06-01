"""Configuration settings for the Mindmap India project."""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.absolute()

# Data paths
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CACHE_DIR = BASE_DIR / "cache"

# Ensure directories exist
for directory in [DATA_DIR, OUTPUT_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

# File paths
CAREERS_CSV = DATA_DIR / "careers.csv"
CLUSTER_MODEL_PATH = CACHE_DIR / "cluster_model.joblib"
VECTORIZER_PATH = CACHE_DIR / "tfidf_vectorizer.joblib"

# Clustering parameters
CLUSTERING_PARAMS = {
    "n_clusters": 5,
    "random_state": 42,
    "n_init": 10
}

# UMAP parameters
UMAP_PARAMS = {
    "n_components": 2,
    "random_state": 42,
    "n_neighbors": 15,
    "min_dist": 0.1,
    "metric": "cosine"
}

# Visualization settings
PLOTLY_THEME = {
    'background': '#121212',
    'text': '#F5F5DC',
    'primary': '#A67B5B',
    'secondary': '#4B3621',
    'accent': '#D4A76A',
    'dark': '#1E1E1E',
    'light': '#2D2D2D',
    'plot_bgcolor': '#1E1E1E',
    'paper_bgcolor': '#121212',
    'font': {'color': '#F5F5DC'}
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': OUTPUT_DIR / 'mindmap.log',
            'formatter': 'standard',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'mindmap': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
