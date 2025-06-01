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
    # Set up output directory
    os.makedirs('../output', exist_ok=True)
    
    # 1. Load and prepare data
    print("Loading data...")
    df = pd.read_csv('../data/careers.csv')
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
    kmeans = KMeans(n_clusters=5, random_state=42)
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
    fig.write_html('../output/career_clusters.html')

    # 6. Create word clouds for each cluster
    print("Generating word clouds...")
    os.makedirs('../output/wordclouds', exist_ok=True)
    for cluster in sorted(df['cluster'].unique()):
        plt.figure(figsize=(10, 6))
        text = ' '.join(df[df['cluster'] == cluster]['combined_features'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Cluster {cluster} - Common Terms')
        plt.savefig(f'../output/wordclouds/cluster_{cluster}_wordcloud.png', bbox_inches='tight', dpi=300)
        plt.close()

    # 7. Save results
    df.to_csv('../output/clustered_careers.csv', index=False)
    print("\nDone! Check the 'output' folder for results.")
    print("1. Open 'output/career_clusters.html' in your browser")
    print("2. Check 'output/wordclouds/' for cluster word clouds")
    print("3. See 'output/clustered_careers.csv' for the full data")

if __name__ == "__main__":
    main()
