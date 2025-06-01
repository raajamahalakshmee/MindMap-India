"""Main application module for the Mindmap India project."""
import os
import logging
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

from config import (
    DATA_DIR, 
    OUTPUT_DIR, 
    CACHE_DIR,
    CLUSTERING_PARAMS,
    UMAP_PARAMS,
    PLOTLY_THEME
)
from .clustering import CareerClusterer, cluster_careers
from .visualization import MindmapVisualizer
from .utils import load_data, save_model, load_model, validate_data

# Configure logging
logger = logging.getLogger(__name__)

class MindmapApp:
    """Main application class for the Mindmap India web app."""
    
    def __init__(self):
        """Initialize the application."""
        self.data = None
        self.clusterer = None
        self.visualizer = MindmapVisualizer()
        self._setup_page_config()
    
    def _setup_page_config(self) -> None:
        """Set up the page configuration."""
        st.set_page_config(
            page_title="Mindmap India",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown(
            f"""
            <style>
                .main {{
                    background-color: {PLOTLY_THEME['plot_bgcolor']};
                    color: {PLOTLY_THEME['text']};
                }}
                .stButton>button {{
                    background-color: {PLOTLY_THEME['primary']};
                    color: {PLOTLY_THEME['text']};
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 0.25rem;
                }}
                .stButton>button:hover {{
                    background-color: {PLOTLY_THEME['accent']};
                    color: {PLOTLY_THEME['text']};
                }}
                .stTextInput>div>div>input {{
                    background-color: {PLOTLY_THEME['dark']};
                    color: {PLOTLY_THEME['text']};
                }}
                .stSelectbox>div>div>div>div {{
                    background-color: {PLOTLY_THEME['dark']};
                    color: {PLOTLY_THEME['text']};
                }}
                .stSlider>div>div>div>div {{
                    background-color: {PLOTLY_THEME['primary']};
                }}
                .stProgress>div>div>div>div {{
                    background-color: {PLOTLY_THEME['accent']};
                }}
                .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
                    color: {PLOTLY_THEME['text']};
                }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    def load_data(self) -> bool:
        """Load the careers data.
        
        Returns:
            bool: True if data was loaded successfully, False otherwise
        """
        try:
            self.data = load_data()
            return True
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            logger.exception("Error loading data")
            return False
    
    def run_clustering(self, n_clusters: int = 5, use_cache: bool = True) -> bool:
        """Run the clustering pipeline.
        
        Args:
            n_clusters: Number of clusters to form
            use_cache: Whether to use cached model if available
            
        Returns:
            bool: True if clustering was successful, False otherwise
        """
        if self.data is None:
            st.error("No data loaded. Please load data first.")
            return False
        
        model_path = CACHE_DIR / f"career_clusterer_{n_clusters}.joblib"
        
        # Try to load from cache if enabled
        if use_cache and model_path.exists():
            try:
                with st.spinner("Loading cached model..."):
                    self.clusterer = CareerClusterer.load(model_path)
                    logger.info(f"Loaded model from cache: {model_path}")
                    return True
            except Exception as e:
                logger.warning(f"Error loading cached model: {str(e)}")
        
        # Run clustering
        with st.spinner("Running clustering... This may take a few minutes."):
            try:
                # Update clustering parameters
                clustering_params = CLUSTERING_PARAMS.copy()
                clustering_params['n_clusters'] = n_clusters
                
                # Run clustering
                self.data, self.clusterer = cluster_careers(
                    self.data,
                    n_clusters=n_clusters,
                    random_state=42
                )
                
                # Save the model
                os.makedirs(CACHE_DIR, exist_ok=True)
                self.clusterer.save(model_path)
                logger.info(f"Saved model to {model_path}")
                
                return True
                
            except Exception as e:
                st.error(f"Error running clustering: {str(e)}")
                logger.exception("Error running clustering")
                return False
    
    def render_sidebar(self) -> Dict[str, Any]:
        """Render the sidebar and return user inputs.
        
        Returns:
            Dict[str, Any]: Dictionary of user inputs
        """
        st.sidebar.title("Mindmap India")
        st.sidebar.markdown("---")
        
        # Data loading
        st.sidebar.subheader("Data")
        if st.sidebar.button("Load Data"):
            with st.spinner("Loading data..."):
                if self.load_data():
                    st.sidebar.success("Data loaded successfully!")
        
        # Clustering options
        st.sidebar.subheader("Clustering")
        n_clusters = st.sidebar.slider(
            "Number of clusters",
            min_value=2,
            max_value=15,
            value=5,
            step=1
        )
        
        use_cache = st.sidebar.checkbox("Use cached model if available", value=True)
        
        if st.sidebar.button("Run Clustering"):
            if self.run_clustering(n_clusters=n_clusters, use_cache=use_cache):
                st.sidebar.success("Clustering completed successfully!")
        
        # Visualization options
        st.sidebar.subheader("Visualization")
        show_wordclouds = st.sidebar.checkbox("Show word clouds", value=True)
        show_parallel_categories = st.sidebar.checkbox("Show parallel categories", value=True)
        
        # Filtering
        st.sidebar.subheader("Filters")
        domains = ["All"] + sorted(self.data['Domain'].unique().tolist()) if self.data is not None and 'Domain' in self.data.columns else ["All"]
        selected_domain = st.sidebar.selectbox("Filter by domain", domains, index=0)
        
        return {
            'n_clusters': n_clusters,
            'show_wordclouds': show_wordclouds,
            'show_parallel_categories': show_parallel_categories,
            'selected_domain': selected_domain
        }
    
    def render_main_content(self, filters: Dict[str, Any]) -> None:
        """Render the main content area.
        
        Args:
            filters: Dictionary of user inputs from the sidebar
        """
        st.title("🧠 Mindmap India")
        st.markdown("Explore career paths and discover new opportunities based on your skills and interests.")
        
        if self.data is None:
            st.info("Please load the data using the sidebar.")
            return
        
        # Apply filters
        filtered_data = self.data.copy()
        if filters['selected_domain'] != "All":
            filtered_data = filtered_data[filtered_data['Domain'] == filters['selected_domain']]
        
        # Show data summary
        st.subheader("Data Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Careers", len(self.data))
        col2.metric("Domains", self.data['Domain'].nunique())
        col3.metric("Filtered Careers", len(filtered_data))
        
        # Show cluster visualization if available
        if self.clusterer is not None and hasattr(self.clusterer, 'embeddings_'):
            st.subheader("Career Clusters")
            
            # Create the plot
            fig = self.visualizer.plot_clusters(
                filtered_data,
                x_col='umap_x',
                y_col='umap_y',
                color_col='cluster',
                hover_cols=['Career', 'Domain', 'Skills'],
                title='Career Clusters Visualization'
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Show word clouds if enabled
            if filters['show_wordclouds'] and 'combined_features' in filtered_data.columns:
                st.subheader("Cluster Word Clouds")
                
                # Create a row of columns for the word clouds
                n_cols = min(3, filters['n_clusters'])
                cols = st.columns(n_cols)
                
                for i in range(filters['n_clusters']):
                    cluster_texts = ' '.join(
                        filtered_data[filtered_data['cluster'] == i]['combined_features']
                    )
                    
                    with cols[i % n_cols]:
                        st.markdown(f"**Cluster {i}**")
                        self.visualizer.create_word_cloud(
                            cluster_texts,
                            max_words=30,
                            width=300,
                            height=200
                        )
            
            # Show parallel categories plot if enabled
            if filters['show_parallel_categories'] and all(col in filtered_data.columns for col in ['Domain', 'Education Level', 'Experience Level']):
                st.subheader("Career Pathways")
                fig = self.visualizer.plot_parallel_categories(
                    filtered_data,
                    dimensions=['Domain', 'Education Level', 'Experience Level']
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def run(self) -> None:
        """Run the application."""
        # Render the sidebar and get user inputs
        filters = self.render_sidebar()
        
        # Render the main content
        self.render_main_content(filters)

def main():
    """Main entry point for the application."""
    # Create and run the app
    app = MindmapApp()
    app.run()

if __name__ == "__main__":
    main()
