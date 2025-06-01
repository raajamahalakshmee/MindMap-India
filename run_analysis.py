import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import umap.umap_ as umap
from wordcloud import WordCloud
import plotly.express as px

def main():
    print("Loading data...")
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data', 'careers.csv')
    output_dir = os.path.join(script_dir, '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    df = pd.read_csv(data_path)
    df['combined_features'] = df['Career'] + ' ' + df['Skills'] + ' ' + df['Description']
    print(f"Loaded {len(df)} careers")
    
    # Text Vectorization
    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X = vectorizer.fit_transform(df['combined_features'])
    
    # Dimensionality Reduction
    print("Reducing dimensions...")
    reducer = umap.UMAP(random_state=42)
    X_umap = reducer.fit_transform(X)
    df['x'] = X_umap[:, 0]
    df['y'] = X_umap[:, 1]
    
    # Clustering
    print("Clustering...")
    n_clusters = min(5, len(df) - 1)  # Ensure we don't have more clusters than samples
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_umap)
    
    # Save results
    output_csv = os.path.join(output_dir, 'clustered_careers.csv')
    df.to_csv(output_csv, index=False)
    print(f"Results saved to: {output_csv}")
    
    # Create visualization
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
    
    # Save interactive plot
    output_html = os.path.join(output_dir, 'career_clusters.html')
    fig.write_html(output_html)
    print(f"Interactive plot saved to: {output_html}")
    
    # Create word clouds
    print("Generating word clouds...")
    wordclouds_dir = os.path.join(output_dir, 'wordclouds')
    os.makedirs(wordclouds_dir, exist_ok=True)
    
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
    
    print("\nAnalysis complete!")
    print(f"1. Open this file in your browser: {os.path.abspath(output_html)}")
    print(f"2. Word clouds are saved in: {os.path.abspath(wordclouds_dir)}")
    print(f"3. Clustered data saved to: {os.path.abspath(output_csv)}")

if __name__ == "__main__":
    main()
