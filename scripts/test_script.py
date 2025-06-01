print("Testing Python script execution...")
try:
    import pandas as pd
    print("Pandas is installed!")
    print(f"Pandas version: {pd.__version__}")
    
    # Test file reading
    import os
    if os.path.exists('../data/careers.csv'):
        df = pd.read_csv('../data/careers.csv')
        print("\nFirst few rows of careers.csv:")
        print(df.head())
    else:
        print("\nError: careers.csv not found at ../data/careers.csv")
        print("Current working directory:", os.getcwd())
        print("Contents of data directory:", os.listdir('../data/'))
        
except Exception as e:
    print(f"\nError: {str(e)}")
    
input("\nPress Enter to exit...")
