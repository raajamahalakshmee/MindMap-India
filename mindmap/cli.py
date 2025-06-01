"""Command-line interface for the Mindmap India package."""
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, List

import pandas as pd

from .clustering import CareerClusterer, cluster_careers
from .visualization import MindmapVisualizer
from .utils import load_data, save_model, load_model

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mindmap_cli.log')
    ]
)
logger = logging.getLogger(__name__)

def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: List of command-line arguments
        
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Mindmap India - Career Exploration Tool')
    
    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Cluster command
    cluster_parser = subparsers.add_parser('cluster', help='Cluster careers')
    cluster_parser.add_argument(
        '--input', 
        type=str, 
        default='data/careers.csv',
        help='Path to input CSV file (default: data/careers.csv)'
    )
    cluster_parser.add_argument(
        '--output', 
        type=str, 
        default='output/clustered_careers.csv',
        help='Path to save clustered data (default: output/clustered_careers.csv)'
    )
    cluster_parser.add_argument(
        '--n-clusters', 
        type=int, 
        default=5,
        help='Number of clusters to create (default: 5)'
    )
    cluster_parser.add_argument(
        '--model', 
        type=str, 
        default=None,
        help='Path to save/load the trained model (default: None)'
    )
    cluster_parser.add_argument(
        '--visualize', 
        action='store_true',
        help='Generate visualizations'
    )
    
    # Visualize command
    visualize_parser = subparsers.add_parser('visualize', help='Generate visualizations')
    visualize_parser.add_argument(
        '--input', 
        type=str, 
        required=True,
        help='Path to input CSV file with clustered data'
    )
    visualize_parser.add_argument(
        '--output-dir', 
        type=str, 
        default='output',
        help='Directory to save visualizations (default: output)'
    )
    
    # Serve command
    serve_parser = subparsers.add_parser('serve', help='Start the web interface')
    serve_parser.add_argument(
        '--port', 
        type=int, 
        default=8501,
        help='Port to run the server on (default: 8501)'
    )
    serve_parser.add_argument(
        '--host', 
        type=str, 
        default='0.0.0.0',
        help='Host to run the server on (default: 0.0.0.0)'
    )
    
    return parser.parse_args(args)

def cluster_command(args: argparse.Namespace) -> int:
    """Handle the cluster command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        # Create output directory if it doesn't exist
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load data
        logger.info(f"Loading data from {args.input}")
        df = load_data(args.input)
        
        # Check if model should be loaded
        if args.model and Path(args.model).exists():
            logger.info(f"Loading model from {args.model}")
            clusterer = CareerClusterer.load(args.model)
            clusters = clusterer.predict(df['combined_features'].fillna('').astype(str).tolist())
            df['cluster'] = clusters
        else:
            # Train new model
            logger.info(f"Training new model with {args.n_clusters} clusters")
            df, clusterer = cluster_careers(
                df,
                n_clusters=args.n_clusters,
                save_path=args.model
            )
        
        # Save results
        logger.info(f"Saving results to {args.output}")
        df.to_csv(args.output, index=False)
        
        # Generate visualizations if requested
        if args.visualize:
            logger.info("Generating visualizations")
            visualizer = MindmapVisualizer()
            
            # Create output directory
            vis_dir = Path('output/visualizations')
            vis_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate cluster plot
            if 'umap_x' in df.columns and 'umap_y' in df.columns:
                fig = visualizer.plot_clusters(
                    df,
                    x_col='umap_x',
                    y_col='umap_y',
                    color_col='cluster',
                    title='Career Clusters'
                )
                fig.write_html(str(vis_dir / 'clusters.html'))
            
            # Generate word clouds for each cluster
            if 'combined_features' in df.columns:
                for cluster_id in df['cluster'].unique():
                    cluster_text = ' '.join(df[df['cluster'] == cluster_id]['combined_features'])
                    visualizer.create_word_cloud(
                        cluster_text,
                        max_words=50,
                        width=800,
                        height=600,
                        save_path=f'wordcloud_cluster_{cluster_id}.png'
                    )
        
        logger.info("Clustering completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Error in cluster command: {str(e)}", exc_info=True)
        return 1

def visualize_command(args: argparse.Namespace) -> int:
    """Handle the visualize command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        # Load data
        logger.info(f"Loading data from {args.input}")
        df = pd.read_csv(args.input)
        
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize visualizer
        visualizer = MindmapVisualizer()
        
        # Generate cluster plot if coordinates are available
        if all(col in df.columns for col in ['umap_x', 'umap_y', 'cluster']):
            fig = visualizer.plot_clusters(
                df,
                x_col='umap_x',
                y_col='umap_y',
                color_col='cluster',
                title='Career Clusters'
            )
            fig.write_html(str(output_dir / 'clusters.html'))
            logger.info(f"Saved cluster plot to {output_dir / 'clusters.html'}")
        
        # Generate word clouds if text data is available
        if 'combined_features' in df.columns and 'cluster' in df.columns:
            for cluster_id in df['cluster'].unique():
                cluster_text = ' '.join(df[df['cluster'] == cluster_id]['combined_features'])
                output_path = output_dir / f'wordcloud_cluster_{cluster_id}.png'
                visualizer.create_word_cloud(
                    cluster_text,
                    max_words=50,
                    width=800,
                    height=600,
                    save_path=str(output_path)
                )
                logger.info(f"Saved word cloud to {output_path}")
        
        logger.info("Visualization completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Error in visualize command: {str(e)}", exc_info=True)
        return 1

def serve_command(args: argparse.Namespace) -> int:
    """Handle the serve command.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code (0 if successful, 1 otherwise)
    """
    try:
        import subprocess
        import webbrowser
        import time
        
        # Start the Streamlit server
        cmd = [
            'streamlit', 'run', 
            '--server.port', str(args.port),
            '--server.address', args.host,
            '--server.headless', 'true',
            '--logger.level', 'info',
            'run.py'
        ]
        
        logger.info(f"Starting server on {args.host}:{args.port}")
        logger.info("Press Ctrl+C to stop the server")
        
        # Open the browser
        url = f"http://{args.host}:{args.port}"
        webbrowser.open(url)
        
        # Run the server
        subprocess.run(cmd)
        return 0
        
    except Exception as e:
        logger.error(f"Error in serve command: {str(e)}", exc_info=True)
        return 1

def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.
    
    Args:
        args: Command-line arguments (default: None, which uses sys.argv[1:])
        
    Returns:
        int: Exit code (0 if successful, non-zero otherwise)
    """
    if args is None:
        args = sys.argv[1:]
    
    # Parse arguments
    parsed_args = parse_args(args)
    
    # Dispatch to appropriate command handler
    if parsed_args.command == 'cluster':
        return cluster_command(parsed_args)
    elif parsed_args.command == 'visualize':
        return visualize_command(parsed_args)
    elif parsed_args.command == 'serve':
        return serve_command(parsed_args)
    else:
        logger.error(f"Unknown command: {parsed_args.command}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
