"""Visualization utilities for the Mindmap India project."""
import logging
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from config import PLOTLY_THEME, OUTPUT_DIR
from .utils import save_plot

logger = logging.getLogger(__name__)

class MindmapVisualizer:
    """Class for creating visualizations for the Mindmap India project."""
    
    def __init__(self, theme: Optional[Dict[str, Any]] = None):
        """Initialize the visualizer with a theme.
        
        Args:
            theme: Custom theme dictionary. If None, uses the default theme.
        """
        self.theme = theme or PLOTLY_THEME
        self.set_plotly_theme()
    
    def set_plotly_theme(self) -> None:
        """Set the default Plotly theme."""
        # Update the default template
        template = go.layout.Template()
        
        # Update layout
        template.layout.plot_bgcolor = self.theme['plot_bgcolor']
        template.layout.paper_bgcolor = self.theme['paper_bgcolor']
        template.layout.font = {'color': self.theme['text']}
        
        # Update traces
        template.data.scatter = [
            go.Scatter(marker=dict(line=dict(width=1, color=self.theme['light']))),
        ]
        
        # Update axes
        template.layout.xaxis = dict(
            showgrid=True, 
            gridcolor=self.theme['dark'],
            linecolor=self.theme['light'],
            zerolinecolor=self.theme['light']
        )
        template.layout.yaxis = dict(
            showgrid=True, 
            gridcolor=self.theme['dark'],
            linecolor=self.theme['light'],
            zerolinecolor=self.theme['light']
        )
        
        # Set the template
        px.defaults.template = template
    
    def plot_clusters(
        self,
        df: pd.DataFrame,
        x_col: str = 'x',
        y_col: str = 'y',
        color_col: str = 'cluster',
        hover_cols: Optional[List[str]] = None,
        title: str = 'Career Clusters',
        width: int = 1200,
        height: int = 800,
        save_path: Optional[str] = None
    ) -> go.Figure:
        """Create an interactive scatter plot of career clusters.
        
        Args:
            df: DataFrame containing the data
            x_col: Name of the x-axis column
            y_col: Name of the y-axis column
            color_col: Name of the column to use for coloring points
            hover_cols: List of columns to show in hover tooltip
            title: Plot title
            width: Plot width in pixels
            height: Plot height in pixels
            save_path: If provided, save the plot to this path
            
        Returns:
            go.Figure: The Plotly figure object
        """
        if hover_cols is None:
            hover_cols = ['Career', 'Domain', 'Skills']
            
        # Ensure required columns exist
        required_cols = [x_col, y_col, color_col] + hover_cols
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Create the figure
        fig = px.scatter(
            df, 
            x=x_col, 
            y=y_col,
            color=color_col,
            hover_name='Career',
            hover_data=hover_cols,
            title=title,
            width=width,
            height=height,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=24, color=self.theme['text'])
            ),
            xaxis_title="UMAP 1",
            yaxis_title="UMAP 2",
            legend_title="Cluster",
            plot_bgcolor=self.theme['plot_bgcolor'],
            paper_bgcolor=self.theme['paper_bgcolor'],
            font=dict(color=self.theme['text']),
            margin=dict(l=20, r=20, t=80, b=20),
        )
        
        # Save if path is provided
        if save_path:
            save_plot(fig, save_path)
            
        return fig
    
    def create_word_cloud(
        self,
        text: str,
        max_words: int = 100,
        width: int = 800,
        height: int = 600,
        save_path: Optional[str] = None
    ) -> None:
        """Create a word cloud from text.
        
        Args:
            text: The text to generate the word cloud from
            max_words: Maximum number of words to include
            width: Width of the output image
            height: Height of the output image
            save_path: If provided, save the word cloud to this path
        """
        # Create a color function based on the theme
        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            colors = [
                self.theme['primary'],
                self.theme['accent'],
                self.theme['secondary']
            ]
            return np.random.choice(colors)
        
        # Generate the word cloud
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=self.theme['plot_bgcolor'],
            max_words=max_words,
            contour_width=1,
            contour_color=self.theme['primary'],
            color_func=color_func
        ).generate(text)
        
        # Display the word cloud
        plt.figure(figsize=(width/100, height/100), facecolor=self.theme['plot_bgcolor'])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save if path is provided
        if save_path:
            plt.savefig(
                OUTPUT_DIR / save_path,
                facecolor=self.theme['plot_bgcolor'],
                bbox_inches='tight',
                pad_inches=0.1
            )
            logger.info(f"Word cloud saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_parallel_categories(
        self,
        df: pd.DataFrame,
        dimensions: Optional[List[str]] = None,
        color_col: str = 'cluster',
        title: str = 'Career Pathways',
        width: int = 1200,
        height: int = 800,
        save_path: Optional[str] = None
    ) -> go.Figure:
        """Create a parallel categories plot.
        
        Args:
            df: DataFrame containing the data
            dimensions: List of column names to use as dimensions
            color_col: Name of the column to use for coloring
            title: Plot title
            width: Plot width in pixels
            height: Plot height in pixels
            save_path: If provided, save the plot to this path
            
        Returns:
            go.Figure: The Plotly figure object
        """
        if dimensions is None:
            dimensions = ['Domain', 'Education Level', 'Experience Level']
            
        # Ensure required columns exist
        required_cols = dimensions + [color_col]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            logger.warning(f"Missing columns for parallel categories plot: {missing_cols}")
            dimensions = [col for col in dimensions if col in df.columns]
            if not dimensions:
                raise ValueError("No valid dimensions provided for parallel categories plot")
        
        # Create the figure
        fig = px.parallel_categories(
            df,
            dimensions=dimensions,
            color=df[color_col],
            title=title,
            width=width,
            height=height,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center',
                font=dict(size=24, color=self.theme['text'])
            ),
            plot_bgcolor=self.theme['plot_bgcolor'],
            paper_bgcolor=self.theme['paper_bgcolor'],
            font=dict(color=self.theme['text']),
            margin=dict(l=20, r=20, t=80, b=20),
        )
        
        # Save if path is provided
        if save_path:
            save_plot(fig, save_path)
            
        return fig

# Create a default instance for convenience
visualizer = MindmapVisualizer()
