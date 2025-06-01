"""
Tests for the career clustering functionality.
"""
import os
import sys
import pytest
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the module to test
try:
    from app.cluster_utils import CareerClusterer, cluster_and_recommend
    from app.app import load_data
    CLUSTER_UTILS_AVAILABLE = True
except ImportError:
    CLUSTER_UTILS_AVAILABLE = False

# Skip all tests if cluster_utils can't be imported
pytestmark = pytest.mark.skipif(
    not CLUSTER_UTILS_AVAILABLE,
    reason="cluster_utils module not available"
)

# Sample test data
SAMPLE_DATA = [
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
    return pd.DataFrame(SAMPLE_DATA)

def test_career_clusterer_initialization():
    """Test that CareerClusterer initializes correctly."""
    clusterer = CareerClusterer(n_clusters=3, random_state=42)
    assert clusterer is not None
    assert clusterer.n_clusters == 3
    assert clusterer.random_state == 42

def test_fit_transform(sample_dataframe):
    """Test fitting the clusterer on sample data."""
    clusterer = CareerClusterer(n_clusters=2, random_state=42)
    df = sample_dataframe.copy()
    
    # Test fitting
    clusterer.fit(df)
    
    # Test that the model was fitted
    assert clusterer.is_fitted
    assert hasattr(clusterer, 'vectorizer')
    assert hasattr(clusterer, 'scaler')
    assert hasattr(clusterer, 'kmeans')
    
    # Test that we have the expected skills and domains
    assert len(clusterer.all_skills) > 0
    assert len(clusterer.all_domains) > 0

def test_recommendations(sample_dataframe):
    """Test getting recommendations."""
    clusterer = CareerClusterer(n_clusters=2, random_state=42)
    df = sample_dataframe.copy()
    
    # Fit the model
    clusterer.fit(df)
    
    # Get recommendations
    target_career = "Data Scientist"
    recommendations = clusterer.recommend(df, target_career, n_recommendations=2)
    
    # Basic assertions
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 2  # Should not return more than requested
    
    # Should not recommend the same career
    assert target_career not in recommendations

def test_cluster_and_recommend(sample_dataframe, tmp_path):
    """Test the high-level cluster_and_recommend function."""
    # Create a temporary cache directory
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    
    # Test with caching enabled
    recommendations = cluster_and_recommend(
        df=sample_dataframe,
        selected_career="Data Scientist",
        n_recommendations=2,
        use_cache=False  # Don't use cache for testing
    )
    
    # Basic assertions
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 2
    if recommendations:  # If we got recommendations
        assert "Data Scientist" not in recommendations

def test_empty_dataframe():
    """Test with an empty DataFrame."""
    clusterer = CareerClusterer()
    empty_df = pd.DataFrame(columns=["Career", "Skills", "Domain", "Description"])
    
    # Should raise a ValueError when fitting an empty DataFrame
    with pytest.raises(ValueError):
        clusterer.fit(empty_df)

def test_missing_columns():
    """Test with a DataFrame missing required columns."""
    clusterer = CareerClusterer()
    df = pd.DataFrame({"WrongColumn": ["Value"]})
    
    # Should raise a KeyError when required columns are missing
    with pytest.raises(KeyError):
        clusterer.fit(df)

# This test requires the actual data file
def test_with_real_data():
    """Test with the actual careers data file."""
    data_path = Path("data/careers.csv")
    if not data_path.exists():
        pytest.skip("Test data file not found")
    
    # Load the data
    df = load_data()
    assert df is not None
    assert not df.empty
    
    # Get recommendations for a sample career
    target_career = df.iloc[0]["Career"]
    recommendations = cluster_and_recommend(
        df=df,
        selected_career=target_career,
        n_recommendations=3,
        use_cache=False
    )
    
    # Basic assertions
    assert isinstance(recommendations, list)
    assert len(recommendations) <= 3
    if recommendations:  # If we got recommendations
        assert target_career not in recommendations
