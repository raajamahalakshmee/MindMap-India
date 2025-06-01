import os
import webbrowser
from pathlib import Path

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'output'
    html_file = output_dir / 'career_clusters.html'
    
    print(f"Looking for visualization file at: {html_file}")
    
    if not html_file.exists():
        print("Error: career_clusters.html not found in the output directory.")
        print("Please run the career clustering script first.")
        return
    
    print(f"Opening {html_file} in default web browser...")
    try:
        # Convert to file URI for better compatibility
        file_uri = html_file.absolute().as_uri()
        webbrowser.open(file_uri)
        print("Visualization should now be open in your default web browser.")
    except Exception as e:
        print(f"Error opening the file: {e}")
        print("\nYou can manually open the file by navigating to:")
        print(f"{html_file.absolute()}")
        print("\nAnd opening it with a web browser.")

if __name__ == "__main__":
    main()
