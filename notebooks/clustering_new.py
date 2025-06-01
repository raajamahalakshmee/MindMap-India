# %%
# Career Clustering Analysis
# This notebook demonstrates the clustering of careers based on their descriptions and skills

# %% [markdown]
# Career Clustering Analysis
# 
# This notebook demonstrates how careers can be clustered based on their descriptions and skills using various machine learning techniques.

# %%
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.manifold import TSNE
import umap.umap_ as umap
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# Set the color scheme to match our black and coffee theme
COFFEE_THEME = {
    'background': '#121212',
    'text': '#F5F5DC',
    'primary': '#A67B5B',
    'secondary': '#4B3621',
    'accent': '#D4A76A',
    'dark': '#1E1E1E',
    'light': '#2D2D2D'
}

# Set the style for matplotlib
plt.style.use('dark_background')
sns.set_palette([COFFEE_THEME['primary'], COFFEE_THEME['accent'], COFFEE_THEME['light']])

# %%
# Load and preprocess the data
def load_data():
    """Load and preprocess the careers data."""
    df = pd.read_csv('../data/careers.csv')
    
    # Create a combined text feature for better clustering
    df['combined_features'] = df['Career'] + ' ' + df['Skills'] + ' ' + df['Description']
    
    return df

# Load the data
df = load_data()
print(f"Loaded {len(df)} careers")

# %%
# Text Vectorization
print("Vectorizing text features...")
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(df['combined_features'])

# %%
# Dimensionality Reduction with UMAP
print("Reducing dimensions with UMAP...")
reducer = umap.UMAP(
    n_components=2, 
    random_state=42,
    n_neighbors=min(15, len(df)-1),
    min_dist=0.1,
    metric='cosine'
)

# Fit and transform the data
X_umap = reducer.fit_transform(X)

# Add UMAP coordinates to the dataframe
df['umap_x'] = X_umap[:, 0]
df['umap_y'] = X_umap[:, 1]

# %%
# Determine optimal number of clusters using the Elbow method
def find_optimal_clusters(X, max_clusters=10):
    """Find the optimal number of clusters using the Elbow method."""
    inertias = []
    K = range(2, min(max_clusters + 1, len(df)))
    
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)
    
    # Plot the Elbow curve
    plt.figure(figsize=(10, 6))
    plt.plot(K, inertias, 'o-', color=COFFEE_THEME['accent'], linewidth=2)
    plt.title('Elbow Method For Optimal k', color=COFFEE_THEME['text'])
    plt.xlabel('Number of Clusters (k)', color=COFFEE_THEME['text'])
    plt.ylabel('Inertia', color=COFFEE_THEME['text'])
    plt.xticks(K)
    plt.grid(True, color=COFFEE_THEME['light'], alpha=0.3)
    plt.gca().set_facecolor(COFFEE_THEME['dark'])
    plt.gcf().set_facecolor(COFFEE_THEME['background'])
    plt.tick_params(colors=COFFEE_THEME['text'])
    
    # Add a vertical line at the suggested k (elbow point)
    if len(K) > 1:
        # Simple elbow detection (can be improved)
        deltas = np.diff(inertias)
        deltas2 = np.diff(deltas)
        elbow = np.argmax(deltas) + 2  # +2 because we start from k=2
        plt.axvline(x=elbow, color=COFFEE_THEME['primary'], linestyle='--', 
                   label=f'Suggested k = {elbow}')
        plt.legend()
    
    plt.show()
    
    return inertias

# Find optimal clusters
print("Finding optimal number of clusters...")
inertias = find_optimal_clusters(X_umap)

# %%
# K-Means Clustering
# Using the suggested number of clusters or a default
optimal_k = 5  # Default, can be adjusted based on the elbow plot
if len(inertias) > 1:
    deltas = np.diff(inertias)
    deltas2 = np.diff(deltas)
    optimal_k = np.argmax(deltas) + 2  # +2 because we start from k=2

print(f"Performing K-Means clustering with k={optimal_k}...")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_umap)
df['cluster'] = clusters

# Calculate silhouette score
silhouette_avg = silhouette_score(X_umap, clusters)
print(f'Silhouette Score: {silhouette_avg:.3f}')

# %%
# Visualize the clusters with Plotly
def plot_clusters_plotly(df):
    """Create an interactive 2D visualization of the clusters using Plotly."""
    fig = px.scatter(
        df, 
        x='umap_x', 
        y='umap_y',
        color='cluster',
        hover_name='Career',
        hover_data=['Domain', 'Skills'],
        title='Career Clusters Visualization',
        color_continuous_scale=[COFFEE_THEME['secondary'], COFFEE_THEME['primary'], COFFEE_THEME['accent']],
        labels={'umap_x': 'UMAP 1', 'umap_y': 'UMAP 2'},
        width=1000,
        height=700
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor=COFFEE_THEME['background'],
        paper_bgcolor=COFFEE_THEME['dark'],
        font_color=COFFEE_THEME['text'],
        title_font_color=COFFEE_THEME['accent'],
        xaxis=dict(showgrid=True, gridcolor=COFFEE_THEME['light'], gridwidth=0.5),
        yaxis=dict(showgrid=True, gridcolor=COFFEE_THEME['light'], gridwidth=0.5),
        legend=dict(
            bgcolor=COFFEE_THEME['dark'],
            bordercolor=COFFEE_THEME['light'],
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor=COFFEE_THEME['dark'],
            font_size=12,
            font_family="Arial"
        )
    )
    
    # Add cluster annotations
    for cluster in sorted(df['cluster'].unique()):
        cluster_data = df[df['cluster'] == cluster]
        fig.add_annotation(
            x=cluster_data['umap_x'].mean(),
            y=cluster_data['umap_y'].max() + 0.2,
            text=f"Cluster {cluster}",
            showarrow=False,
            font=dict(color=COFFEE_THEME['accent'], size=12)
        )
    
    return fig

# Display the interactive plot
print("Generating interactive visualization...")
fig = plot_clusters_plotly(df)
fig.show()

# %%
# Word Clouds for Each Cluster
def generate_word_clouds(df, cluster_col='cluster', text_col='combined_features', max_words=50):
    """Generate word clouds for each cluster."""
    n_clusters = df[cluster_col].nunique()
    
    # Set up the figure
    fig, axes = plt.subplots((n_clusters + 1) // 2, 2, figsize=(16, 4 * ((n_clusters + 1) // 2)))
    if n_clusters <= 2:
        axes = np.array([axes])
    axes = axes.flatten()
    
    for i, cluster in enumerate(sorted(df[cluster_col].unique())):
        ax = axes[i]
        cluster_text = ' '.join(df[df[cluster_col] == cluster][text_col])
        
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color=COFFEE_THEME['background'],
            colormap='YlOrBr',  # Coffee-like colors
            max_words=max_words,
            contour_width=1,
            contour_color=COFFEE_THEME['primary']
        ).generate(cluster_text)
        
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_title(f'Cluster {cluster} - {len(df[df[cluster_col] == cluster])} careers', 
                    color=COFFEE_THEME['accent'], fontsize=12)
        ax.axis('off')
    
    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')
    
    plt.tight_layout()
    plt.suptitle('Word Clouds for Each Cluster', y=1.02, color=COFFEE_THEME['text'], fontsize=16)
    plt.show()

# Generate and display word clouds
print("Generating word clouds for each cluster...")
generate_word_clouds(df)

# %%
# Cluster Analysis
def analyze_clusters(df, cluster_col='cluster'):
    """Analyze and display statistics for each cluster."""
    cluster_stats = []
    
    for cluster in sorted(df[cluster_col].unique()):
        cluster_data = df[df[cluster_col] == cluster]
        
        # Get top domains in this cluster
        top_domains = cluster_data['Domain'].value_counts().head(3)
        domains_str = ', '.join([f"{domain} ({count})" for domain, count in top_domains.items()])
        
        # Get most common skills
        all_skills = [skill.strip() for skills in cluster_data['Skills'].str.split(',') for skill in skills]
        top_skills = pd.Series(all_skills).value_counts().head(5)
        skills_str = ', '.join([f"{skill} ({count})" for skill, count in top_skills.items()])
        
        cluster_stats.append({
            'Cluster': cluster,
            'Number of Careers': len(cluster_data),
            'Top Domains': domains_str,
            'Top Skills': skills_str,
            'Example Careers': ', '.join(cluster_data['Career'].sample(min(3, len(cluster_data)), random_state=42))
        })
    
    return pd.DataFrame(cluster_stats)

# Display cluster analysis
print("Analyzing clusters...")
cluster_analysis = analyze_clusters(df)
print("\nCluster Analysis:")
print(cluster_analysis.to_string(index=False, max_colwidth=50))

# %%
# Save the clustered data
df.to_csv('../data/careers_clustered.csv', index=False)
print("\nClustered data saved to 'data/careers_clustered.csv'")

# %%
# Interactive Parallel Categories Plot
def plot_parallel_categories(df):
    """Create an interactive parallel categories plot."""
    # Prepare the data
    plot_df = df[['Career', 'Domain', 'cluster']].copy()
    plot_df['cluster'] = 'Cluster ' + plot_df['cluster'].astype(str)
    
    # Create the figure
    fig = px.parallel_categories(
        plot_df,
        dimensions=['Domain', 'cluster'],
        color_continuous_scale=[COFFEE_THEME['secondary'], COFFEE_THEME['primary']],
        title='Career Domains and Clusters',
        labels={'Domain': 'Domain', 'cluster': 'Cluster'}
    )
    
    # Update layout
    fig.update_layout(
        plot_bgcolor=COFFEE_THEME['background'],
        paper_bgcolor=COFFEE_THEME['dark'],
        font_color=COFFEE_THEME['text'],
        title_font_color=COFFEE_THEME['accent'],
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

# Display the parallel categories plot
print("\nGenerating parallel categories plot...")
fig = plot_parallel_categories(df)
fig.show()

print("\nAnalysis complete! Check the visualizations above for insights.")
