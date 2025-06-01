"""
Shared test fixtures and configuration for pytest.
"""
import pytest
import pandas as pd
from pathlib import Path

# Add the parent directory to the path so we can import app modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Sample test data for reuse across tests
SAMPLE_CAREERS = [
    {
        "Career": "Data Scientist",
        "Skills": "Python, Machine Learning, Statistics",
        "Domain": "Technology",
        "Description": "Analyzes complex data to extract insights using ML"
    },
    {
        "Career": "Software Engineer",
        "Skills": "Python, Java, Algorithms",
        "Domain": "Technology",
        "Description": "Develops software applications and systems"
    },
    {
        "Career": "Data Analyst",
        "Skills": "SQL, Excel, Statistics",
        "Domain": "Business",
        "Description": "Analyzes data to help with business decisions"
    },
    {
        "Career": "Marketing Manager",
        "Skills": "Marketing, Communication, Analytics",
        "Domain": "Business",
        "Description": "Develops marketing strategies and campaigns"
    },
    {
        "Career": "Mechanical Engineer",
        "Skills": "CAD, Physics, Mathematics",
        "Domain": "Engineering",
        "Description": "Designs and analyzes mechanical systems"
    }
]

@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(SAMPLE_CAREERS)

@pytest.fixture
def sample_career_names():
    """Return a list of sample career names."""
    return [career["Career"] for career in SAMPLE_CAREERS]

@pytest.fixture
def sample_skills():
    """Return a set of unique skills from the sample data."""
    skills = set()
    for career in SAMPLE_CAREERS:
        skills.update(skill.strip() for skill in career["Skills"].split(","))
    return skills

@pytest.fixture
def sample_domains():
    """Return a set of unique domains from the sample data."""
    return {career["Domain"] for career in SAMPLE_CAREERS}

@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create a temporary cache directory for testing."""
    cache_dir = tmp_path / "test_cache"
    cache_dir.mkdir()
    return cache_dir
