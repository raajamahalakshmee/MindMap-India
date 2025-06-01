"""Clustering functionality for the Mindmap India project."""
import logging
from typing import Dict, Any, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import umap.umap_ as umap
import joblib

from config import CLUSTERING_PARAMS, UMAP_PARAMS, CACHE_DIR
from .utils import save_model, load_model, validate_data

logger = logging.getLogger(__name__)

class CareerClusterer:
    """Class for clustering careers based on their features."""
    
    def __init__(
        self, 
        n_clusters: int = 5,
        random_state: int = 42,
        n_init: int = 10,
        umap_params: Optional[Dict[str, Any]] = None,
        vectorizer_params: Optional[Dict[str, Any]] = None
    ):
        """Initialize the CareerClusterer.
        
        Args:
            n_clusters: Number of clusters to form
            random_state: Random state for reproducibility
            n_init: Number of time the k-means algorithm will be run with different centroid seeds
            umap_params: Parameters for UMAP dimensionality reduction
            vectorizer_params: Parameters for TF-IDF vectorizer
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.n_init = n_init
        
        # Set default parameters if not provided
        self.umap_params = umap_params or UMAP_PARAMS
        self.vectorizer_params = vectorizer_params or {
            'stop_words': 'english',
            'max_features': 1000,
            'ngram_range': (1, 2)
        }
        
        # Initialize models
        self.vectorizer = TfidfVectorizer(**self.vectorizer_params)
        self.reducer = umap.UMAP(**self.umap_params)
        self.clusterer = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=n_init
        )
        
        # Placeholders for fitted attributes
        self.feature_names_ = None
        self.cluster_centers_ = None
        self.labels_ = None
        self.embeddings_ = None
    
    def fit(self, texts: List[str]) -> 'CareerClusterer':
        """Fit the clustering pipeline on the input texts.
        
        Args:
            texts: List of text documents to cluster
            
        Returns:
            self: The fitted CareerClusterer instance
        """
        logger.info(f"Fitting CareerClusterer on {len(texts)} documents")
        
        # Vectorize the text
        logger.debug("Vectorizing text...")
        X = self.vectorizer.fit_transform(texts)
        self.feature_names_ = self.vectorizer.get_feature_names_out()
        
        # Reduce dimensionality
        logger.debug("Reducing dimensions...")
        self.embeddings_ = self.reducer.fit_transform(X)
        
        # Cluster the reduced data
        logger.debug("Clustering...")
        self.labels_ = self.clusterer.fit_predict(self.embeddings_)
        self.cluster_centers_ = self.clusterer.cluster_centers_
        
        logger.info(f"Clustering complete. Found {len(np.unique(self.labels_))} clusters")
        return self
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """Transform new data into the cluster space.
        
        Args:
            texts: List of text documents to transform
            
        Returns:
            np.ndarray: Cluster assignments for the input texts
        """
        if not hasattr(self, 'vectorizer') or not hasattr(self, 'reducer') or not hasattr(self, 'clusterer'):
            raise RuntimeError("Model has not been fitted yet. Call 'fit' first.")
        
        # Transform the text
        X = self.vectorizer.transform(texts)
        
        # Reduce dimensions
        X_umap = self.reducer.transform(X)
        
        # Predict clusters
        return self.clusterer.predict(X_umap)
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Fit the model and return cluster assignments.
        
        Args:
            texts: List of text documents to cluster
            
        Returns:
            np.ndarray: Cluster assignments for the input texts
        """
        return self.fit(texts).labels_
    
    def get_top_features_per_cluster(
        self, 
        n_features: int = 10,
        feature_names: Optional[List[str]] = None
    ) -> Dict[int, List[Tuple[str, float]]]:
        """Get the top features for each cluster.
        
        Args:
            n_features: Number of top features to return per cluster
            feature_names: List of feature names. If None, uses the vectorizer's feature names
            
        Returns:
            Dict[int, List[Tuple[str, float]]]: Dictionary mapping cluster indices to lists of 
                (feature_name, importance) tuples
        """
        if not hasattr(self, 'clusterer') or self.cluster_centers_ is None:
            raise RuntimeError("Model has not been fitted yet. Call 'fit' first.")
        
        if feature_names is None:
            if not hasattr(self, 'feature_names_') or self.feature_names_ is None:
                raise ValueError("No feature names available. Provide feature_names or fit the model first.")
            feature_names = self.feature_names_
        
        top_features = {}
        
        # Get the cluster centers (in the original feature space)
        # For KMeans, the centers are already in the original space
        cluster_centers = self.cluster_centers_
        
        # For each cluster, get the top features
        for i in range(self.n_clusters):
            center = cluster_centers[i]
            top_indices = np.argsort(center)[::-1][:n_features]
            top_features[i] = [
                (feature_names[idx], center[idx])
                for idx in top_indices
            ]
        
        return top_features
    
    def save(self, filepath: str) -> None:
        """Save the model to disk.
        
        Args:
            filepath: Path to save the model to
        """
        model_data = {
            'n_clusters': self.n_clusters,
            'random_state': self.random_state,
            'n_init': self.n_init,
            'umap_params': self.umap_params,
            'vectorizer_params': self.vectorizer_params,
            'feature_names_': self.feature_names_,
            'cluster_centers_': self.cluster_centers_,
            'labels_': self.labels_,
            'embeddings_': self.embeddings_
        }
        
        # Save the model data
        joblib.dump(model_data, filepath)
        
        # Save the vectorizer and reducer separately
        vectorizer_path = str(filepath).replace('.joblib', '_vectorizer.joblib')
        reducer_path = str(filepath).replace('.joblib', '_reducer.joblib')
        clusterer_path = str(filepath).replace('.joblib', '_clusterer.joblib')
        
        joblib.dump(self.vectorizer, vectorizer_path)
        joblib.dump(self.reducer, reducer_path)
        joblib.dump(self.clusterer, clusterer_path)
        
        logger.info(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'CareerClusterer':
        """Load a model from disk.
        
        Args:
            filepath: Path to the saved model
            
        Returns:
            CareerClusterer: The loaded model
        """
        # Load the model data
        model_data = joblib.load(filepath)
        
        # Create a new instance
        clusterer = cls(
            n_clusters=model_data['n_clusters'],
            random_state=model_data['random_state'],
            n_init=model_data['n_init'],
            umap_params=model_data['umap_params'],
            vectorizer_params=model_data['vectorizer_params']
        )
        
        # Load the vectorizer and reducer
        vectorizer_path = str(filepath).replace('.joblib', '_vectorizer.joblib')
        reducer_path = str(filepath).replace('.joblib', '_reducer.joblib')
        clusterer_path = str(filepath).replace('.joblib', '_clusterer.joblib')
        
        clusterer.vectorizer = joblib.load(vectorizer_path)
        clusterer.reducer = joblib.load(reducer_path)
        clusterer.clusterer = joblib.load(clusterer_path)
        
        # Set the fitted attributes
        clusterer.feature_names_ = model_data['feature_names_']
        clusterer.cluster_centers_ = model_data['cluster_centers_']
        clusterer.labels_ = model_data['labels_']
        clusterer.embeddings_ = model_data['embeddings_']
        
        logger.info(f"Model loaded from {filepath}")
        return clusterer

def cluster_careers(
    df: pd.DataFrame,
    text_col: str = 'combined_features',
    n_clusters: int = 5,
    random_state: int = 42,
    save_path: Optional[str] = None
) -> Tuple[pd.DataFrame, CareerClusterer]:
    """Cluster careers based on their features.
    
    Args:
        df: DataFrame containing career data
        text_col: Name of the column containing text to cluster on
        n_clusters: Number of clusters to form
        random_state: Random state for reproducibility
        save_path: If provided, save the trained model to this path
        
    Returns:
        Tuple containing:
            - DataFrame with cluster assignments added
            - Fitted CareerClusterer instance
    """
    # Validate input
    validate_data(df, required_columns=[text_col])
    
    # Initialize the clusterer
    clusterer = CareerClusterer(
        n_clusters=n_clusters,
        random_state=random_state
    )
    
    # Fit the model and get cluster assignments
    texts = df[text_col].fillna('').astype(str).tolist()
    cluster_labels = clusterer.fit_transform(texts)
    
    # Add cluster assignments to the DataFrame
    df = df.copy()
    df['cluster'] = cluster_labels
    
    # Add UMAP coordinates if available
    if hasattr(clusterer, 'embeddings_') and clusterer.embeddings_ is not None:
        df['umap_x'] = clusterer.embeddings_[:, 0]
        df['umap_y'] = clusterer.embeddings_[:, 1]
    
    # Save the model if path is provided
    if save_path:
        clusterer.save(save_path)
    
    return df, clusterer
