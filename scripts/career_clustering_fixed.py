import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import umap.umap_ as umap
from wordcloud import WordCloud
import plotly.express as px

def main():
    try:
        # Get the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set up paths
        base_dir = os.path.dirname(script_dir)
        data_path = os.path.join(base_dir, 'data', 'careers.csv')
        output_dir = os.path.join(base_dir, 'output')
        wordclouds_dir = os.path.join(output_dir, 'wordclouds')
        
        print(f"Script directory: {script_dir}")
        print(f"Base directory: {base_dir}")
        print(f"Data path: {data_path}")
        
        # Create output directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(wordclouds_dir, exist_ok=True)
        
        # 1. Load and prepare data
        print("\nLoading data...")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Could not find data file at: {data_path}")
            
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} careers")
        
        df['combined_features'] = df['Career'] + ' ' + df['Skills'] + ' ' + df['Description']

        # 2. Text Vectorization
        print("Vectorizing text...")
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(df['combined_features'])

        # 3. Dimensionality Reduction
        print("Reducing dimensions...")
        reducer = umap.UMAP(random_state=42)
        X_umap = reducer.fit_transform(X)
        df['x'] = X_umap[:, 0]
        df['y'] = X_umap[:, 1]

        # 4. Clustering
        print("Clustering...")
        kmeans = KMeans(n_clusters=min(5, len(df)-1), random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(X_umap)

        # 5. Visualize with Plotly
        print("Creating visualization...")
        fig = px.scatter(
            df, 
            x='x', y='y',
            color='cluster',
            hover_name='Career',
            hover_data=['Domain', 'Skills'],
            title='Career Clusters Visualization',
            width=1200,
            height=800
        )
        
        output_html = os.path.join(output_dir, 'career_clusters.html')
        fig.write_html(output_html)
        print(f"Saved visualization to: {output_html}")

        # 6. Create word clouds for each cluster
        print("\nGenerating word clouds...")
        for cluster in sorted(df['cluster'].unique()):
            plt.figure(figsize=(10, 6))
            text = ' '.join(df[df['cluster'] == cluster]['combined_features'])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Cluster {cluster} - Common Terms')
            
            wordcloud_path = os.path.join(wordclouds_dir, f'cluster_{cluster}_wordcloud.png')
            plt.savefig(wordcloud_path, bbox_inches='tight', dpi=300)
            plt.close()
            print(f"Saved word cloud for cluster {cluster}")

        # 7. Save results
        output_csv = os.path.join(output_dir, 'clustered_careers.csv')
        df.to_csv(output_csv, index=False)
        
        print("\n" + "="*50)
        print("ANALYSIS COMPLETE!")
        print("="*50)
        print(f"\nResults saved to: {output_dir}")
        print(f"1. Open this file in your browser: {os.path.abspath(output_html)}")
        print(f"2. Word clouds saved in: {os.path.abspath(wordclouds_dir)}")
        print(f"3. Full clustered data: {os.path.abspath(output_csv)}")
        
    except Exception as e:
        print("\n" + "!"*50)
        print("ERROR OCCURRED:")
        print("!"*50)
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        print("\nCurrent working directory:", os.getcwd())
        print("\nDirectory contents:")
        for root, dirs, files in os.walk('.'):
            level = root.replace('.', '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files[:5]:  # Show first 5 files in each directory
                print(f"{subindent}{f}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")

        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
