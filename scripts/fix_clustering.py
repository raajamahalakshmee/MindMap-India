import os
import shutil
from pathlib import Path
import streamlit as st
import pandas as pd
from app.cluster_utils import cluster_and_recommend

def main():
    print("Fixing clustering issues...")
    
    # Clear the cache directory
    cache_dir = Path('cache')
    if cache_dir.exists():
        print(f"Removing existing cache directory: {cache_dir}")
        shutil.rmtree(cache_dir)
    
    # Create a new cache directory
    cache_dir.mkdir(exist_ok=True)
    print(f"Created new cache directory: {cache_dir}")
    
    # Load the data
    data_path = Path('data/careers.csv')
    if not data_path.exists():
        print(f"Error: Data file not found at {data_path}")
        return
    
    print(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    
    # Test clustering with a sample career
    test_career = 'Data Scientist' if 'Data Scientist' in df['Career'].values else df['Career'].iloc[0]
    print(f"\nTesting clustering with career: {test_career}")
    
    try:
        recommendations = cluster_and_recommend(
            df=df,
            selected_career=test_career,
            n_recommendations=5,
            use_cache=False  # Force recreation of the model
        )
        
        print("\nClustering successful! Recommendations:")
        for i, career in enumerate(recommendations, 1):
            print(f"{i}. {career}")
            
        print("\nYou can now run the Streamlit app again.")
        print("Run: streamlit run app/app.py")
        
    except Exception as e:
        print(f"\nError during clustering: {str(e)}")
        print("\nPlease check the error message above and ensure all dependencies are installed.")
        print("Make sure you have run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
