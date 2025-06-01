import os
import sys
import platform

def main():
    print("="*50)
    print("PYTHON ENVIRONMENT CHECK")
    print("="*50)
    
    # Python info
    print("\nPython Version:", sys.version)
    print("Python Executable:", sys.executable)
    print("Platform:", platform.platform())
    
    # Current working directory
    cwd = os.getcwd()
    print("\nCurrent Working Directory:", cwd)
    
    # List directory contents
    print("\nDirectory Contents:")
    for item in os.listdir('.'):
        print(f"- {item} {'(DIR)' if os.path.isdir(item) else ''}")
    
    # Check for data directory
    data_dir = os.path.join(cwd, 'data')
    print("\nChecking for data directory:", data_dir)
    if os.path.exists(data_dir):
        print("Data directory exists! Contents:")
        for item in os.listdir(data_dir):
            print(f"- {item}")
    else:
        print("Data directory does not exist!")
    
    # Check for careers.csv
    careers_path = os.path.join(data_dir, 'careers.csv')
    print("\nChecking for careers.csv:", careers_path)
    if os.path.exists(careers_path):
        print("careers.csv found!")
    else:
        print("careers.csv not found!")
    
    # Check imports
    print("\nTesting imports:")
    try:
        import pandas as pd
        print("- pandas:", pd.__version__)
    except ImportError:
        print("- pandas: NOT INSTALLED")
    
    try:
        import sklearn
        print("- scikit-learn:", sklearn.__version__)
    except ImportError:
        print("- scikit-learn: NOT INSTALLED")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
