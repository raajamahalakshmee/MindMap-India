import pandas as pd
from pathlib import Path

def main():
    data_path = Path('data/careers.csv')
    print(f"Checking data at: {data_path.absolute()}")
    
    try:
        # Check if file exists
        if not data_path.exists():
            print(f"Error: File not found at {data_path.absolute()}")
            return
            
        # Try to load the data
        df = pd.read_csv(data_path)
        print("\nData loaded successfully!")
        print(f"\nNumber of careers: {len(df)}")
        print("\nFirst 5 careers:")
        print(df[['Career', 'Domain']].head().to_string(index=False))
        
        # Check for required columns
        required_columns = {'Career', 'Skills', 'Domain', 'Description'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            print(f"\nMissing required columns: {', '.join(missing_columns)}")
        else:
            print("\nAll required columns are present!")
            
        # Check for missing values
        print("\nMissing values per column:")
        print(df[list(required_columns)].isna().sum())
        
    except Exception as e:
        print(f"\nError loading data: {str(e)}")

if __name__ == "__main__":
    main()
