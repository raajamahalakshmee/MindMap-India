import os
import re
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.exceptions import NotFittedError

# Cache directory for storing models and vectorizers
CACHE_DIR = Path('cache')
CACHE_DIR.mkdir(exist_ok=True)

class CareerClusterer:
    """A class to handle career clustering and recommendations with caching."""
    
    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        """Initialize the career clusterer.
        
        Args:
            n_clusters: Number of clusters to create
            random_state: Random state for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
        self.scaler = StandardScaler()
        self.kmeans = KMeans(
            n_clusters=n_clusters, 
            random_state=random_state, 
            n_init=10
        )
        self.is_fitted = False
        self.all_skills = []
        self.all_domains = []
    
    def save(self, path: Path) -> None:
        """Save the model to disk."""
        joblib.dump({
            'vectorizer': self.vectorizer,
            'scaler': self.scaler,
            'kmeans': self.kmeans,
            'all_skills': self.all_skills,
            'all_domains': self.all_domains,
            'is_fitted': self.is_fitted
        }, path)
    
    @classmethod
    def load(cls, path: Path) -> 'CareerClusterer':
        """Load a model from disk."""
        data = joblib.load(path)
        clusterer = cls(n_clusters=data['kmeans'].n_clusters, random_state=data['kmeans'].random_state)
        clusterer.vectorizer = data['vectorizer']
        clusterer.scaler = data['scaler']
        clusterer.kmeans = data['kmeans']
        clusterer.all_skills = data['all_skills']
        clusterer.all_domains = data['all_domains']
        clusterer.is_fitted = data['is_fitted']
        return clusterer

    @staticmethod
    def preprocess_text(text: str) -> str:
        """Basic text preprocessing.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        return text
    
    def _get_skills_vector(self, skills):
        """Convert skills to a vector based on all possible skills.
        
        Args:
            skills: Can be a string of comma-separated skills, a list, or None
            
        Returns:
            List[int]: Binary vector indicating presence of each skill
        """
        if not skills or (isinstance(skills, (list, tuple)) and not skills):
            return [0] * len(self.all_skills) if self.all_skills else []
            
        try:
            # Handle string input
            if isinstance(skills, str):
                skills_list = [s.strip().lower() for s in skills.split(',')]
            # Handle list-like input
            elif hasattr(skills, '__iter__') and not isinstance(skills, str):
                skills_list = [str(s).strip().lower() for s in skills]
            else:
                skills_list = [str(skills).strip().lower()]
                
            # Create binary vector
            return [1 if skill in skills_list else 0 for skill in self.all_skills]
            
        except Exception as e:
            print(f"Error creating skills vector: {str(e)}")
            return [0] * len(self.all_skills) if self.all_skills else []
    
    def _get_domain_encoding(self, domain) -> List[int]:
        """One-hot encode domain.
        
        Args:
            domain: Domain string or value to encode
            
        Returns:
            List[int]: One-hot encoded domain vector
        """
        if not self.all_domains:
            return []
            
        try:
            if pd.isna(domain) or not domain:
                return [0] * len(self.all_domains)
                
            domain_str = str(domain).strip().lower()
            
            # Try exact match first
            if domain_str in self.all_domains:
                return [1 if d == domain_str else 0 for d in self.all_domains]
                
            # Try case-insensitive match
            domain_lower = [d.lower() for d in self.all_domains]
            if domain_str in domain_lower:
                idx = domain_lower.index(domain_str)
                return [1 if i == idx else 0 for i in range(len(self.all_domains))]
                
            # No match found
            return [0] * len(self.all_domains)
            
        except Exception as e:
            print(f"Error encoding domain '{domain}': {str(e)}")
            return [0] * len(self.all_domains)

    def fit(self, df: pd.DataFrame) -> 'CareerClusterer':
        """Fit the clusterer on career data.
        
        Args:
            df: DataFrame containing career data
            
        Returns:
            self: Fitted clusterer instance
        """
        # Preprocess data
        df = df.copy()
        df['Description'] = df['Description'].apply(self.preprocess_text)
        
        # Get all unique skills and domains
        try:
            # First, ensure we're working with strings and handle missing values
            skills_series = df['Skills'].fillna('').astype(str)
            
            # Split skills and clean them
            all_skills = set()
            for skills_str in skills_series:
                if skills_str and str(skills_str).lower() not in ['nan', 'none', '']:
                    # Split by comma and clean each skill
                    skills = [s.strip().lower() for s in str(skills_str).split(',')]
                    all_skills.update([s for s in skills if s])  # Add non-empty skills
            
            self.all_skills = sorted(list(all_skills))
            
            if not self.all_skills:
                print("Warning: No skills found in the dataset")
                self.all_skills = []
                
        except Exception as e:
            print(f"Error processing skills: {str(e)}")
            self.all_skills = []
        
        self.all_domains = sorted(df['Domain'].dropna().unique())
        
        # Create feature vectors
        description_vectors = self.vectorizer.fit_transform(df['Description']).toarray()
        
        # Create skills matrix
        skills_matrix = np.array([
            self._get_skills_vector(skills) if pd.notna(skills) \
                else [0] * len(self.all_skills)
            for skills in df['Skills']
        ])
        
        # Create domain matrix
        domain_matrix = np.array([
            self._get_domain_encoding(domain) if pd.notna(domain) \
                else [0] * len(self.all_domains)
            for domain in df['Domain']
        ])
        
        # Combine all features
        X = np.hstack([description_vectors, skills_matrix, domain_matrix])
        
        # Scale features and fit KMeans
        X_scaled = self.scaler.fit_transform(X)
        self.kmeans.fit(X_scaled)
        
        self.is_fitted = True
        return self
    
    def recommend(self, df: pd.DataFrame, selected_career: str, 
                 n_recommendations: int = 5) -> List[str]:
        """Get recommendations for a given career.
        
        Args:
            df: DataFrame containing career data
            selected_career: The career to find recommendations for
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended career names
        """
        print(f"\n=== Starting recommendation for: {selected_career} ===")
        
        try:
            if not self.is_fitted:
                error_msg = "Error: Clusterer not fitted. Call 'fit' first."
                print(error_msg)
                return [error_msg]
            
            # Ensure we're working with a clean copy of the data
            df = df.copy()
            print(f"Working with {len(df)} careers in the dataset")
            
            # Clean and preprocess the data
            df['Career'] = df['Career'].astype(str).str.strip()
            print(f"Unique careers after cleaning: {df['Career'].nunique()}")
            
            # Handle missing descriptions
            if 'Description' not in df.columns:
                df['Description'] = ''
            df['Description'] = df['Description'].astype(str).apply(self.preprocess_text)
            
            # Find the target career
            selected_career = str(selected_career).strip()
            print(f"Looking for career: '{selected_career}'")
            
            if selected_career not in df['Career'].values:
                error_msg = f"Error: Career '{selected_career}' not found in database. " \
                          f"Available careers: {', '.join(df['Career'].head(5).tolist())}..."
                print(error_msg)
                return [error_msg]
                
            # Get the target career's index
            target_idx = df[df['Career'] == selected_career].index[0]
            print(f"Found target career at index {target_idx}")
            
            # Transform features
            try:
                description_vectors = self.vectorizer.transform(df['Description']).toarray()
                print(f"Description vectors shape: {description_vectors.shape}")
            except Exception as e:
                error_msg = f"Error transforming descriptions: {str(e)}"
                print(error_msg)
                return [error_msg]
            
            # Create skills matrix
            print(f"Processing skills for {len(df)} careers...")
            if 'Skills' not in df.columns:
                df['Skills'] = ''
                
            skills_matrix = np.zeros((len(df), len(self.all_skills)))
            for i, skills in enumerate(df['Skills'].fillna('')):
                try:
                    if pd.notna(skills) and str(skills).strip():
                        skills_matrix[i] = self._get_skills_vector(str(skills))
                except Exception as e:
                    print(f"Error processing skills for index {i}: {str(e)}")
            print(f"Skills matrix shape: {skills_matrix.shape}")
            
            # Create domain matrix
            print(f"Processing domains for {len(df)} careers...")
            if 'Domain' not in df.columns:
                df['Domain'] = ''
                
            domain_matrix = np.zeros((len(df), len(self.all_domains)))
            for i, domain in enumerate(df['Domain'].fillna('')):
                try:
                    if pd.notna(domain) and str(domain).strip():
                        domain_matrix[i] = self._get_domain_encoding(str(domain))
                except Exception as e:
                    print(f"Error processing domain for index {i}: {str(e)}")
            print(f"Domain matrix shape: {domain_matrix.shape}")
            
            # Combine features and scale
            try:
                X = np.hstack([
                    description_vectors, 
                    skills_matrix, 
                    domain_matrix
                ])
                print(f"Combined features shape: {X.shape}")
                
                X_scaled = self.scaler.transform(X)
                print(f"Scaled features shape: {X_scaled.shape}")
            except Exception as e:
                error_msg = f"Error combining or scaling features: {str(e)}"
                print(error_msg)
                return [error_msg]
            
            # Get cluster assignments
            try:
                cluster_labels = self.kmeans.predict(X_scaled)
                print(f"Cluster labels shape: {cluster_labels.shape}")
                print(f"Unique clusters: {np.unique(cluster_labels)}")
            except Exception as e:
                error_msg = f"Error predicting clusters: {str(e)}"
                print(error_msg)
                return [error_msg]
            
            # Find careers in the same cluster
            target_cluster = cluster_labels[target_idx]
            cluster_indices = np.where(cluster_labels == target_cluster)[0]
            print(f"Found {len(cluster_indices)} careers in cluster {target_cluster}")
            
            # Calculate similarities within the cluster
            try:
                target_vector = X_scaled[target_idx].reshape(1, -1)
                cluster_vectors = X_scaled[cluster_indices]
                similarities = cosine_similarity(target_vector, cluster_vectors)[0]
                print(f"Calculated similarities for {len(similarities)} careers")
            except Exception as e:
                error_msg = f"Error calculating similarities: {str(e)}"
                print(error_msg)
                return [error_msg]
                
            print("=== Recommendation calculation complete ===\n")
            
            # Get top similar careers (excluding the selected one)
            similar_indices = np.argsort(similarities)[::-1]
            similar_careers = []
            
            for idx in similar_indices:
                if len(similar_careers) >= n_recommendations:
                    break
                    
                career_idx = cluster_indices[idx]
                career = df.iloc[career_idx]['Career']
                
                # Convert to string and clean
                career = str(career).strip()
                
                if career and career != selected_career and career not in similar_careers:
                    similar_careers.append(career)
                    if len(similar_careers) >= n_recommendations:
                        break
            
            return similar_careers
            
        except Exception as e:
            print(f"Error in recommend: {str(e)}")
            return [f"Error generating recommendations: {str(e)}"]


def cluster_and_recommend(df: pd.DataFrame, selected_career: str, 
                         n_recommendations: int = 5, use_cache: bool = True) -> List[str]:
    """Cluster careers and get recommendations for a selected career.
    
    Args:
        df: DataFrame containing career data
        selected_career: The career to find recommendations for
        n_recommendations: Number of recommendations to return
        use_cache: Whether to use cached model if available
        
    Returns:
        List of recommended career names
    """
    try:
        print(f"Starting recommendation for: {selected_career}")
        
        # Clean the input career name
        selected_career = str(selected_career).strip()
        print(f"Cleaned career name: '{selected_career}'")
        
        # Validate input
        if not selected_career:
            return ["Error: No career selected."]
            
        if 'Career' not in df.columns:
            return ["Error: 'Career' column not found in the dataset."]
            
        # Clean career names in the dataframe
        df = df.copy()
        df['Career'] = df['Career'].astype(str).str.strip()
        
        # Check if career exists
        if selected_career not in df['Career'].values:
            available_careers = df['Career'].head(5).tolist()
            return [
                f"Error: Career '{selected_career}' not found in the dataset. "
                f"Available careers: {', '.join(available_careers)}..."
            ]
        
        # Create cache directory if it doesn't exist
        cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cache')
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, 'career_clusterer.joblib')
        print(f"Using cache path: {cache_path}")
        
        # Initialize clusterer
        clusterer = CareerClusterer()
        
        # Try to load from cache if enabled
        if use_cache and os.path.exists(cache_path):
            try:
                print("Loading model from cache...")
                clusterer = CareerClusterer.load(cache_path)
                print("Successfully loaded model from cache")
            except Exception as e:
                print(f"Error loading cached model: {e}")
                print("Fitting new model...")
                clusterer = CareerClusterer()
                clusterer.fit(df)
                try:
                    clusterer.save(cache_path)
                    print("Saved new model to cache")
                except Exception as save_error:
                    print(f"Error saving model to cache: {save_error}")
        else:
            # Fit a new model if no cache or cache loading failed
            print("Fitting new model (no cache)...")
            clusterer.fit(df)
            if use_cache:
                try:
                    clusterer.save(cache_path)
                    print("Saved new model to cache")
                except Exception as save_error:
                    print(f"Error saving model to cache: {save_error}")
        
        # Get recommendations
        print("Generating recommendations...")
        try:
            recommendations = clusterer.recommend(df, selected_career, n_recommendations)
            print(f"Generated {len(recommendations)} recommendations")
            
            if not recommendations:
                return [f"No recommendations found for '{selected_career}'. Try a different career."]
                
            # Ensure all recommendations are strings
            return [str(rec) for rec in recommendations]
            
        except Exception as e:
            import traceback
            error_msg = f"Error in clusterer.recommend(): {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return [f"Error generating recommendations: {str(e)}"]
            
    except Exception as e:
        import traceback
        error_msg = f"Unexpected error in cluster_and_recommend: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return [f"An unexpected error occurred: {str(e)}"]
