import os
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from typing import Optional, List, Dict, Any

# Set page config first to ensure proper rendering
st.set_page_config(
    page_title="Mindmap India: Career Explorer",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from .cluster_utils import cluster_and_recommend
except ImportError:
    from cluster_utils import cluster_and_recommend

# App version
__version__ = "1.0.0"

# Load custom CSS
def load_css():
    """Load and apply custom CSS styles."""
    css_path = Path(__file__).parent / 'assets' / 'style.css'
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Add custom inline styles with modern dark theme
    st.markdown("""
    <style>
    /* Base styles */
    :root {
        --primary: #6366f1;
        --primary-hover: #4f46e5;
        --bg-dark: #0f172a;
        --bg-darker: #0a0f1e;
        --card-bg: #1e293b;
        --card-hover: #2d3748;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border-color: #2d3748;
        --success: #10b981;
        --info: #3b82f6;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-darker);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    
    /* Base styles */
    .stApp {
        background: linear-gradient(135deg, var(--bg-darker) 0%, var(--bg-dark) 100%);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
    }
    
    /* Main title */
    .main-title {
        color: var(--text-primary);
        text-align: center;
        margin: 1.5rem 0 2rem;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary), #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        position: relative;
        padding-bottom: 1rem;
    }
    
    .main-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), #8b5cf6);
        border-radius: 2px;
    }
    
    /* Career card styles */
    .career-card {
        background: var(--card-bg);
        color: var(--text-primary);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .career-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
        border-color: var(--primary);
    }
    
    /* Recommendation styles */
    .recommendation {
        font-size: 1.1rem;
        margin: 0.75rem 0;
        padding: 1.25rem 1.5rem;
        background: var(--card-bg);
        color: var(--text-primary);
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 4px solid var(--primary);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .recommendation::before {
        content: '→';
        color: var(--primary);
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .recommendation:hover {
        background: var(--card-hover);
        transform: translateX(8px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
    }
    
    /* Form elements */
    .stSelectbox > div > div {
        font-size: 1rem;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        background: var(--card-bg);
        color: var(--text-primary);
        border: 2px solid var(--border-color);
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover, 
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }
    
    .stSelectbox > label {
        color: var(--text-primary) !important;
        font-weight: 500;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%);
        color: white;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        background: linear-gradient(135deg, var(--primary-hover) 0%, #7c3aed 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Alerts and messages */
    .stAlert {
        border-radius: 12px;
        background: var(--card-bg);
        color: var(--text-primary);
        border-left: 4px solid var(--info);
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stAlert [data-testid="stMarkdownContainer"] {
        color: var(--text-primary) !important;
    }
    
    /* Main content */
    .main .block-container {
        max-width: 1200px;
        padding: 2rem 1.5rem;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700;
        margin-top: 1.5em;
        margin-bottom: 0.75em;
        line-height: 1.3;
    }
    
    h1 { font-size: 2.25rem; }
    h2 { font-size: 1.875rem; }
    h3 { font-size: 1.5rem; }
    h4 { font-size: 1.25rem; }
    
    /* Text and links */
    p, div, span {
        color: var(--text-primary) !important;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    a {
        color: var(--primary) !important;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    a:hover {
        text-decoration: underline;
        opacity: 0.9;
    }
    
    /* Expander */
    .stExpander {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .stExpander > label {
        color: var(--text-primary) !important;
        font-weight: 600;
        padding: 1rem 1.5rem;
        background: rgba(99, 102, 241, 0.1);
        border-radius: 12px 12px 0 0;
        margin: 0 !important;
    }
    
    .stExpander > .element-container {
        padding: 1.5rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: var(--bg-darker);
        border-right: 1px solid var(--border-color);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), #8b5cf6);
    }
    
    /* Custom badges */
    .badge {
        display: inline-block;
        padding: 0.35em 0.65em;
        font-size: 0.75em;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 50rem;
        background: var(--primary);
        color: white;
        margin: 0.2rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem 1rem;
        }
        
        .main-title {
            font-size: 2rem;
        }
        
        .recommendation {
            padding: 1rem;
            font-size: 1rem;
        }
    }
    
    /* Animation for loading */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stSpinner > div > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }
    
    .stSpinner > div > div:first-child {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Custom scrollbar for sidebar */
    .css-1oe5cao {
        scrollbar-width: thin;
        scrollbar-color: var(--primary) var(--bg-darker);
    }
    
    .css-1oe5cao::-webkit-scrollbar {
        width: 6px;
    }
    
    .css-1oe5cao::-webkit-scrollbar-track {
        background: var(--bg-darker);
    }
    
    .css-1oe5cao::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data() -> Optional[pd.DataFrame]:
    """Load and return the careers data with validation.
    
    Returns:
        DataFrame with career data or None if loading fails
    """
    try:
        current_dir = Path(__file__).parent
        data_path = current_dir.parent / 'data' / 'careers.csv'
        
        # Check if file exists
        if not data_path.exists():
            st.error(f"Data file not found at: {data_path}")
            return None
            
        # Load and validate data
        df = pd.read_csv(data_path)
        
        # Clean up string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        
        # Check required columns
        required_columns = {'Career', 'Skills', 'Domain', 'Description'}
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            st.error(f"Missing required columns in data: {', '.join(missing_columns)}")
            return None
            
        # Check for missing values in required columns
        missing_values = df[['Career', 'Skills', 'Description']].isna().sum()
        if missing_values.any():
            st.warning(f"Found {missing_values.sum()} missing values in the dataset. Some recommendations may be affected.")
        
        # Ensure Career column has unique values
        if df['Career'].nunique() != len(df):
            st.warning("Found duplicate career names. Keeping the first occurrence.")
            df = df.drop_duplicates(subset=['Career'], keep='first')
            
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.error("Please check that the data file exists and is properly formatted.")
        return None

def clear_cache() -> None:
    """Clear the model cache directory.
    
    This function removes all files in the cache directory to force the app
    to rebuild models with fresh data.
    """
    import shutil
    from pathlib import Path
    
    cache_dir = Path(CACHE_DIR)
    if cache_dir.exists() and cache_dir.is_dir():
        try:
            # Remove all files in the cache directory
            for file_path in cache_dir.glob('*'):
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
            return True
        except Exception as e:
            st.error(f"Error clearing cache: {e}")
            return False
    return True

def display_sidebar(df: pd.DataFrame) -> int:
    """Display the sidebar with app information and controls using dark theme.
    
    Args:
        df: The career dataframe
    
    Returns:
        Number of recommendations to display
    """
    # Add custom CSS for the sidebar with modern design
    st.markdown("""
    <style>
        /* Sidebar base */
        .css-1d391kg {
            background: var(--bg-darker) !important;
            border-right: 1px solid var(--border-color) !important;
            padding: 1.5rem 1rem;
        }
        
        /* Sidebar content */
        .css-1oe5cao {
            padding: 0.5rem 0;
            scrollbar-width: thin;
            scrollbar-color: var(--primary) var(--bg-darker);
        }
        
        /* Sidebar sections */
        .sidebar-section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .sidebar-section:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        }
        
        /* Section headers */
        .sidebar-section h3 {
            color: var(--text-primary);
            margin: 0 0 1rem 0;
            padding-bottom: 0.75rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .sidebar-section h3::before {
            content: '▶';
            font-size: 0.8em;
            color: var(--primary);
            transition: transform 0.2s ease;
        }
        
        .sidebar-section[open] h3::before {
            transform: rotate(90deg);
        }
        
        /* Slider styling */
        .stSlider {
            margin: 1.5rem 0;
        }
        
        .stSlider > div > div > div {
            background: linear-gradient(90deg, var(--primary), #8b5cf6) !important;
        }
        
        .stSlider > div > div > div > div > div {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
        }
        
        .stSlider > div > div > div > div > div:hover {
            border-color: var(--primary-hover) !important;
        }
        
        /* Number input */
        .stNumberInput > div > div > input {
            background: var(--card-bg) !important;
            border: 2px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
        }
        
        /* Select box in sidebar */
        .stSelectbox > div > div {
            background: var(--card-bg) !important;
            border: 2px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1) !important;
            background: linear-gradient(135deg, var(--primary-hover) 0%, #7c3aed 100%) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* Checkbox styling */
        .stCheckbox > label {
            color: var(--text-primary) !important;
        }
        
        .stCheckbox > div > div {
            background: var(--card-bg) !important;
            border: 2px solid var(--border-color) !important;
            border-radius: 6px !important;
        }
        
        .stCheckbox > div > div:hover {
            border-color: var(--primary) !important;
        }
        
        .stCheckbox > div > div > div > div {
            background-color: var(--primary) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # App header with gradient text and icon
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 1.5rem; padding: 1rem 0; border-radius: 12px; 
                        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
                        border: 1px solid var(--border-color);'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🧭</div>
                <h2 style='margin: 0; background: linear-gradient(90deg, var(--primary) 0%, #8b5cf6 100%); 
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    Mindmap India
                </h2>
                <p style='color: var(--text-secondary); margin: 0.25rem 0 0; font-size: 0.95rem; font-weight: 500;'>
                    Career Explorer
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # About section with icon and improved typography
        with st.expander("✨ About", expanded=True):
            st.markdown(
                """
                <div class='sidebar-section'>
                    <p style='color: var(--text-secondary); line-height: 1.7; margin: 0;'>
                        Discover career paths similar to your interests using our AI-powered 
                        recommendation engine that analyzes skills, domains, and career data 
                        to provide personalized career suggestions.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Settings section with improved UI
        with st.expander("⚙️ Settings", expanded=True):
            st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
            
            # Number of recommendations slider with better styling
            st.markdown(
                """
                <div style='margin-bottom: 1.5rem;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                        <span style='color: var(--text-primary); font-weight: 500;'>Recommendations</span>
                        <span id='rec-value' style='background: var(--card-hover); padding: 0.25rem 0.75rem; 
                        border-radius: 12px; font-size: 0.85rem; font-weight: 600; color: var(--primary);'>5</span>
                    </div>
                """,
                unsafe_allow_html=True
            )
            
            num_recommendations = st.slider(
                "Number of recommendations:",
                min_value=1,
                max_value=10,
                value=5,
                label_visibility="collapsed",
                help="Adjust the number of career recommendations to display"
            )
            
            st.markdown(
                "<script>"
                "const slider = document.querySelector('.stSlider input');"
                "const valueDisplay = document.getElementById('rec-value');"
                "slider.addEventListener('input', (e) => {"
                "    valueDisplay.textContent = e.target.value;"
                "});"
                "</script>",
                unsafe_allow_html=True
            )
            
            # Clear cache button with confirmation
            st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
            if st.button("🔄 Clear Cache", key="clear_cache_btn", 
                        help="Clear cached data and refresh recommendations"):
                clear_cache()
                st.success("✓ Cache cleared successfully!")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Data info section with stats
        with st.expander("📊 Dataset", expanded=False):
            st.markdown(
                f"""
                <div class='sidebar-section'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 1rem;'>
                        <div style='text-align: center; padding: 0.75rem; background: rgba(99, 102, 241, 0.1); 
                                    border-radius: 8px; flex: 1; margin: 0 0.25rem;'>
                            <div style='font-size: 1.5rem; font-weight: 700; color: var(--primary);'>{len(df)}</div>
                            <div style='font-size: 0.75rem; color: var(--text-secondary);'>Careers</div>
                        </div>
                        <div style='text-align: center; padding: 0.75rem; background: rgba(99, 102, 241, 0.1); 
                                    border-radius: 8px; flex: 1; margin: 0 0.25rem;'>
                            <div style='font-size: 1.5rem; font-weight: 700; color: var(--primary);'>
                                {df['Domain'].nunique()}
                            </div>
                            <div style='font-size: 0.75rem; color: var(--text-secondary);'>Domains</div>
                        </div>
                    </div>
                    <p style='color: var(--text-secondary); font-size: 0.85rem; line-height: 1.6; margin: 0;'>
                        Our dataset is continuously updated with the latest career information 
                        from trusted educational and occupational sources.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # App info section with version and links
        with st.expander("ℹ️ App Info", expanded=False):
            st.markdown(
                f"""
                <div class='sidebar-section'>
                    <div style='margin-bottom: 1rem;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                            <span style='color: var(--text-secondary);'>Version</span>
                            <span style='color: var(--text-primary); font-weight: 500;'>{__version__}</span>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                            <span style='color: var(--text-secondary);'>Last Updated</span>
                            <span style='color: var(--text-primary);'>2023-11-15</span>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                            <span style='color: var(--text-secondary);'>Data Version</span>
                            <span style='color: var(--text-primary);'>1.0.0</span>
                        </div>
                    </div>
                    <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);'>
                        <a href='#' style='display: inline-flex; align-items: center; color: var(--primary) !important; 
                        text-decoration: none; margin-right: 1rem; font-size: 0.9rem;'>
                            <span style='margin-right: 0.25rem;'>📚</span> Docs
                        </a>
                        <a href='#' style='display: inline-flex; align-items: center; color: var(--primary) !important; 
                        text-decoration: none; margin-right: 1rem; font-size: 0.9rem;'>
                            <span style='margin-right: 0.25rem;'>🐛</span> Report Issue
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Footer with improved styling
        st.markdown(
            """
            <div style='text-align: center; margin-top: 2rem; padding: 1rem 0; 
                        color: var(--text-secondary); font-size: 0.8rem; border-top: 1px solid var(--border-color);'>
                <div style='margin-bottom: 0.5rem;'>
                    <a href='#' style='color: var(--primary) !important; text-decoration: none; margin: 0 0.5rem;'>Terms</a>
                    <span>•</span>
                    <a href='#' style='color: var(--primary) !important; text-decoration: none; margin: 0 0.5rem;'>Privacy</a>
                    <span>•</span>
                    <a href='#' style='color: var(--primary) !important; text-decoration: none; margin: 0 0.5rem;'>Contact</a>
                </div>
                <div>© 2023 Mindmap India. All rights reserved.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return num_recommendations

def display_career_recommendations(selected_career: str, recommendations) -> None:
    """Display career recommendations in the main content area with modern dark theme.
    
    Args:
        selected_career: The career that was selected
        recommendations: List or array of recommended careers with their details
    """
    import numpy as np
    import pandas as pd
    
    # Add India logo to the top right
    st.markdown("""
    <style>
    .logo-container {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    .logo-container img {
        height: 60px;
        width: auto;
    }
    </style>
    <div class="logo-container">
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/1200px-Flag_of_India.svg.png" alt="India Flag">
    </div>
    """, unsafe_allow_html=True)

    # If recommendations is None or empty, show a message and return
    if recommendations is None:
        st.warning("No recommendations available. Please try a different career or check your input.")
        return

    # Convert recommendations to a list if it's a pandas Series or numpy array
    try:
        if hasattr(recommendations, 'tolist'):  # For numpy arrays
            recommendations = recommendations.tolist()
        elif hasattr(recommendations, 'to_dict'):  # For pandas Series/DataFrame
            recommendations = recommendations.to_dict('records')
        
        # If it's a single item, make it a list
        if not isinstance(recommendations, (list, tuple)):
            recommendations = [recommendations]
        
        # Debug information
        st.sidebar.write("Debug Info:")
        st.sidebar.json({
            "type": str(type(recommendations)),
            "length": len(recommendations) if hasattr(recommendations, '__len__') else 'N/A',
            "first_item": str(recommendations[0]) if recommendations else 'Empty'
        })
        
        # Process recommendations
        processed_recommendations = []
        for rec in recommendations:
            try:
                if rec is not None:
                    if isinstance(rec, dict):
                        # If it's already a dictionary, clean it up
                        clean_rec = {k: (v.item() if hasattr(v, 'item') else str(v)) 
                                   for k, v in rec.items() if v is not None}
                        processed_recommendations.append(clean_rec)
                    elif isinstance(rec, str) and rec.lower() not in ['nan', 'none', '']:
                        # If it's a string, create a dictionary with the name
                        processed_recommendations.append({'name': rec.strip()})
                    elif hasattr(rec, 'tolist'):
                        # Handle numpy arrays
                        rec_list = rec.tolist()
                        if isinstance(rec_list, (list, tuple)) and rec_list:
                            processed_recommendations.append({'name': str(rec_list[0])})
                    else:
                        # Convert non-dict items to strings
                        clean_rec = str(rec)
                        if clean_rec.lower() not in ['nan', 'none', '']:
                            processed_recommendations.append({'name': clean_rec})
            except Exception as e:
                print(f"Error processing recommendation {rec}: {str(e)}")
                continue
                        
        if not processed_recommendations:
            st.warning("No valid recommendations found after processing.")
            return
            
    except Exception as e:
        st.error(f"Error processing recommendations: {str(e)}")
        st.exception(e)  # This will show the full traceback in the app
        return
    # Add custom CSS for the recommendations with black and coffee theme
    st.markdown("""
    <style>
        /* Base colors */
        :root {
            --primary: #8B5A2B;  /* Coffee brown */
            --primary-hover: #6B4423;
            --bg-dark: #0A0A0A;  /* Slightly off-black background */
            --bg-darker: #000000;
            --card-bg: #1A1A1A;  /* Slightly lighter black for cards */
            --card-hover: #2A2A2A;
            --text-primary: #F5F5DC;  /* Beige text */
            --text-secondary: #D2B48C;  /* Tan text */
            --border-color: #3E2723;  /* Dark brown border */
            --success: #4CAF50;
            --info: #2196F3;
            --warning: #FF9800;
            --danger: #F44336;
        }
        
        /* Main content background */
        .main .block-container {
            background-color: var(--bg-dark);
            color: var(--text-primary);
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-1y0tads, .st-emotion-cache-1cypcdb {
            background-color: var(--bg-darker) !important;
            color: var(--text-primary) !important;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input {
            background-color: var(--card-bg) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
        }
        
        /* Recommendation cards */
        .career-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border: 1px solid var(--border-color);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
            color: var(--text-primary);
        }
        
        .career-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--primary);
        }
        
        .career-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-color: var(--primary);
        }
        
        .career-card .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .career-card .title {
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding-left: 0.5rem;
            border-left: 3px solid var(--primary);
            margin-left: -1.5rem;
            padding-left: 1rem;
        }
        
        .career-card .domain {
            display: inline-block;
            background: rgba(139, 90, 43, 0.2);
            color: var(--primary);
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0.5rem 0;
            border: 1px solid var(--border-color);
        }
        
        .career-card .skills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1.5rem 0;
            align-items: center;
        }
        
        .career-card .skill-tag {
            background: rgba(139, 90, 43, 0.15);
            color: var(--text-secondary);
            padding: 0.4rem 0.8rem;
            border-radius: 16px;
            font-size: 0.8rem;
            border: 1px solid var(--border-color);
            margin: 0.1rem 0.3rem 0.3rem 0;
            display: inline-block;
            transition: all 0.2s ease;
            white-space: nowrap;
            line-height: 1.4;
        }
        
        .career-card .skill-tag:hover {
            background: rgba(139, 90, 43, 0.3);
            transform: translateY(-2px);
        }
        
        .career-card .description {
            color: var(--text-primary);
            line-height: 1.7;
            margin: 1rem 0;
            font-size: 0.95rem;
            opacity: 0.9;
            white-space: pre-line;
            word-wrap: break-word;
            padding-right: 1rem;
        }
        
        .career-card .description p {
            margin: 0.75rem 0;
            color: var(--text-primary);
            line-height: 1.7;
        }
        
        .career-card .description ul, 
        .career-card .description ol {
            margin: 0.75rem 0;
            padding-left: 1.75rem;
        }
        
        .career-card .description li {
            margin: 0.5rem 0;
            line-height: 1.6;
        }
        
        .career-card .description br {
            content: "";
            display: block;
            margin: 0.5rem 0;
        }
        
        .career-card .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.85rem;
        }
        
        .career-card .similarity {
            font-weight: 700;
            color: var(--primary);
            font-size: 1.1rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .career-card .similarity::before {
            content: '✓';
            color: var(--success);
            font-weight: bold;
        }
        
        .career-card .actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .career-card .action-btn {
            background: rgba(139, 90, 43, 0.2);
            border: 1px solid var(--primary);
            color: var(--text-primary);
            padding: 0.6rem 1.2rem;
            border-radius: 30px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0 0.5rem;
        }
        
        .career-card .action-btn:first-child {
            background: transparent;
        }
        
        .career-card .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        .career-card .action-btn:active {
            transform: translateY(0);
        }
        
        .career-card .action-btn:hover {
            background: var(--bg-darker);
            color: var(--primary);
            border-color: var(--primary);
        }
        
        /* Animation for card entrance */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .career-card {
            animation: fadeInUp 0.4s ease-out forwards;
            opacity: 0;
        }
        
        /* Add delay for each card */
        .career-card:nth-child(1) { animation-delay: 0.1s; }
        .career-card:nth-child(2) { animation-delay: 0.2s; }
        .career-card:nth-child(3) { animation-delay: 0.3s; }
        .career-card:nth-child(4) { animation-delay: 0.4s; }
        .career-card:nth-child(5) { animation-delay: 0.5s; }
    </style>
    """, unsafe_allow_html=True)
    
    # Add a nice header with gradient background
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin: 1.5rem 0 2.5rem 0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    '>
        <div style='position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; 
                    background: rgba(255, 255, 255, 0.1); border-radius: 50%; z-index: 0;'></div>
        <div style='position: relative; z-index: 1;'>
            <div style='display: flex; align-items: center; margin-bottom: 0.75rem;'>
                <div style='background: rgba(255, 255, 255, 0.15); width: 48px; height: 48px; 
                            border-radius: 12px; display: flex; align-items: center; justify-content: center; 
                            margin-right: 1rem;'>
                    <span style='font-size: 1.5rem; color: white;'>💡</span>
                </div>
                <h2 style='margin: 0; color: white; font-size: 1.75rem; font-weight: 700;'>
                    Career Recommendations
                </h2>
            </div>
            <p style='margin: 0; color: rgba(255, 255, 255, 0.9); font-size: 1.05rem; max-width: 80%; line-height: 1.6;'>
                Based on your interest in: <strong style='color: white;'>{selected_career}</strong>
            </p>
            <div style='margin-top: 1rem; display: inline-block; 
                        background: rgba(255, 255, 255, 0.15); 
                        color: white; padding: 0.5rem 1rem; 
                        border-radius: 8px; font-size: 0.9rem;'>
                <span style='margin-right: 0.5rem;'>🔍</span> 
                {len(recommendations)} recommendations found
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not recommendations:
        st.markdown("""
        <div style='background: var(--card-bg); border-radius: 12px; padding: 2rem; 
                    text-align: center; border: 1px dashed var(--border-color); margin: 2rem 0;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🔍</div>
            <h3 style='color: var(--text-primary); margin-bottom: 0.5rem;'>No Recommendations Found</h3>
            <p style='color: var(--text-secondary); margin: 0;'>
                We couldn't find any careers matching your criteria. 
                Try adjusting your filters or select a different career to explore.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Display each recommendation with animation and hover effects
    for i, career in enumerate(processed_recommendations, 1):
        try:
            # Extract career name - handle different possible field names
            career_name = ""
            if isinstance(career, dict):
                # Try different possible field names for the career name
                for field in ['name', 'career', 'title', 'job_title', 'role', 'position', 'Career']:
                    if field in career and career[field] and str(career[field]).lower() not in ['nan', 'none', '']:
                        career_name = str(career[field])
                        break
            
            # If we still don't have a name, try to use the string representation
            if not career_name:
                career_name = str(career)
                if career_name.lower() in ['nan', 'none', '']:
                    continue
            
            # Generate a unique key for each recommendation
            key = f"rec_{i}_{hash(str(career_name)) % 10000}"
            
            # Extract other fields with fallbacks
            domain = ""
            if isinstance(career, dict):
                for field in ['domain', 'Domain', 'category', 'Category']:
                    if field in career and career[field] and str(career[field]).lower() not in ['nan', 'none', '']:
                        domain = str(career[field])
                        break
            domain = domain or "Technology"
            
            # Get description
            description = ""
            if isinstance(career, dict):
                for field in ['description', 'Description', 'desc', 'summary']:
                    if field in career and career[field] and str(career[field]).lower() not in ['nan', 'none', '']:
                        description = str(career[field])
                        break
            
            # Fallback description if none found
            if not description:
                description = f"This career in {domain} involves working with specialized knowledge and skills. " \
                            f"Professionals in this field typically work on projects that require expertise in their domain."
            
            # Clean and escape the description
            from markupsafe import escape
            description = escape(description)
            # Convert newlines to <br> for proper HTML display
            description = description.replace('\n', '<br>')
            
            # Process skills
            skills = []
            if isinstance(career, dict):
                for field in ['skills', 'Skills', 'competencies', 'Competencies']:
                    if field in career and career[field]:
                        skills_data = career[field]
                        if isinstance(skills_data, str):
                            skills = [s.strip() for s in skills_data.split(',') if s.strip()]
                        elif isinstance(skills_data, (list, tuple, set)):
                            skills = [str(s).strip() for s in skills_data if s and str(s).strip()]
                        if skills:
                            break
            
            # Fallback skills if none found
            if not skills:
                skills = ["Problem Solving", "Teamwork", "Communication", "Critical Thinking"]
            
            # Limit the number of skills to display
            max_skills = 5
            display_skills = skills[:max_skills]
            extra_skills = len(skills) - max_skills if len(skills) > max_skills else 0
            
            # Calculate similarity score (placeholder logic)
            similarity = f"{min(95, 100 - ((i-1) * 5))}% match"
            
        except Exception as e:
            st.sidebar.error(f"Error processing recommendation {i}: {str(e)}")
            continue
        
        # Create a card for the recommendation
        from markupsafe import escape
        
        # Create a container for the card
        with st.container():
            # Use columns for layout
            col1, col2 = st.columns([0.85, 0.15])
            
            with col1:
                # Career title with gradient
                st.markdown(f"""
                <h3 style='margin: 0; padding: 0; line-height: 1.3; 
                           background: linear-gradient(90deg, var(--primary), #8b5cf6);
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;
                           font-weight: 700; font-size: 1.3rem;'>
                    {i}. {escape(str(career_name))}
                </h3>
                """, unsafe_allow_html=True)
                
                # Domain
                st.caption(domain)
                
                # Description
                st.markdown(description, unsafe_allow_html=True)
                
                # Skills
                with st.container():
                    skill_tags = "".join(
                        f"<span class='skill-tag'>{escape(str(skill))}</span>" 
                        for skill in display_skills
                    )
                    if extra_skills > 0:
                        skill_tags += f"<span class='skill-tag'>+{extra_skills} more</span>"
                    st.markdown("<div style='margin: 1rem 0;'>" + skill_tags + "</div>", unsafe_allow_html=True)
            
            with col2:
                # Similarity score
                st.markdown(f"""
                <div style='text-align: right; margin-bottom: 0.5rem; 
                            font-weight: 600; color: var(--primary);'>
                    {similarity}
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🔍", key=f"view_{i}", help="View Details"):
                        st.session_state['selected_career'] = career_name
                with col_btn2:
                    if st.button("💼", key=f"jobs_{i}", help="Explore Jobs"):
                        st.session_state['explore_jobs'] = career_name
            
            # Divider between cards
            st.markdown("<hr style='margin: 1.5rem 0; border: 0.5px solid var(--border-color);'/>", 
                      unsafe_allow_html=True)
    
    # Add JavaScript for interactive elements
    st.markdown("""
    <script>
    function showMoreInfo(career) {
        // In a real app, this would show more details about the career
        alert('Showing more details for: ' + career);
    }
    
    // Add hover effect for cards
    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('.career-card');
        cards.forEach(card => {
            card.addEventListener('click', function(e) {
                // Don't trigger if clicking on a button
                if (!e.target.closest('.action-btn')) {
                    this.classList.toggle('expanded');
                }
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

def main() -> None:
    """Main function to run the Streamlit app with modern dark theme."""
    # Load CSS
    load_css()
    
    # Add custom CSS for the entire app
    st.markdown("""
    <style>
        /* Base styles */
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg: #0f172a;
            --bg-darker: #0b1120;
            --card-bg: #1e293b;
            --card-hover: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #2d3748;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
        }
        
        /* Main app container */
        .stApp {
            background: var(--bg);
            color: var(--text-primary);
            min-height: 100vh;
        }
        
        /* Main content area */
        .main .block-container {
            padding: 2rem 2.5rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        /* Links */
        a {
            color: var(--primary);
            text-decoration: none;
            transition: all 0.2s ease;
        }
        
        a:hover {
            color: var(--primary-hover);
            text-decoration: underline;
        }
        
        /* Buttons */
        .stButton > button {
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.25rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* Form elements */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div {
            background: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
        }
        
        /* Tooltips */
        .stTooltip {
            background: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add Font Awesome for icons
    st.markdown(
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">',
        unsafe_allow_html=True
    )
    
    # Add smooth scrolling
    st.markdown("""
    <style>
        html {
            scroll-behavior: smooth;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page header with improved styling
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2.5rem;'>
        <div style='display: inline-flex; align-items: center; background: rgba(99, 102, 241, 0.1); 
                    padding: 0.5rem 1.5rem; border-radius: 50px; margin-bottom: 1rem;'>
            <span style='font-size: 1.25rem; margin-right: 0.75rem;'>🚀</span>
            <span style='font-weight: 600; color: var(--primary);'>BETA</span>
        </div>
        <h1 style='margin: 0.5rem 0 1rem 0; font-size: 2.5rem; background: linear-gradient(90deg, var(--primary), #8b5cf6); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>
            Mindmap India
        </h1>
        <p style='color: var(--text-secondary); font-size: 1.1rem; max-width: 700px; margin: 0 auto 1.5rem; line-height: 1.6;'>
            Discover your ideal career path with AI-powered recommendations based on your skills, 
            interests, and the latest job market trends.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='
        text-align: center; 
        margin-bottom: 30px; 
        color: #bdc3c7;
        font-size: 1.1em;
        padding: 0 10%;
    '>
        <i class='fas fa-search' style='margin-right: 8px; color: #3498db;'></i>
        Discover career paths similar to your interests using AI-powered recommendations
    </div>
    """, unsafe_allow_html=True)
    
    # Add a loading spinner while loading data
    with st.spinner('Loading career data...'):
        df = load_data()
    
    if df is None:
        st.error("Failed to load career data. Please check the data file and try again.")
        return
        
    # Display sidebar and get number of recommendations
    num_recommendations = display_sidebar(df)
    
    # Main content area
    st.markdown("""
    <style>
        /* Main content area styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Card styling for recommendations */
        .recommendation {
            background-color: #2d3436;
            border-radius: 8px;
            padding: 15px 20px;
            margin-bottom: 12px;
            transition: all 0.3s ease;
            border-left: 4px solid #3498db;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .recommendation:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Section headers */
        h2, h3, h4 {
            color: #3498db !important;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #2d3436;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #3498db;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #2980b9;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Career selection in main content with improved UI
    st.markdown("### <i class='fas fa-search' style='margin-right: 10px; color: #3498db;'></i>Select a Career", unsafe_allow_html=True)
    
    # Add search box with custom styling
    search_container = st.container()
    with search_container:
        col1, col2 = st.columns([3, 1])
        with col1:
            try:
                career_options = sorted(df['Career'].unique().tolist())
                default_index = career_options.index('Data Scientist') if 'Data Scientist' in career_options else 0
                
                # Enhanced selectbox with custom styling
                selected_career = st.selectbox(
                    label="Choose a career to explore similar options:",
                    options=career_options,
                    index=default_index,
                    format_func=lambda x: f"{x}" if pd.notna(x) else "",
                    help="Start typing to search for a specific career",
                    key="career_select"
                )
                
                # Get the exact career name from the dataframe
                selected_career = df[df['Career'].str.strip() == str(selected_career).strip()]['Career'].iloc[0]
                
            except Exception as e:
                st.error(f"Error initializing career selection: {str(e)}")
                return
        
        # Add a refresh button
        with col2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 Refresh", key="refresh_btn"):
                st.rerun()
    
    # Add some spacing
    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
    
    # Get recommendations when a career is selected
    if selected_career:
        with st.spinner('Analyzing career paths...'):
            with st.spinner('Finding similar careers...'):
                try:
                    print(f"\n=== Starting recommendation process for: {selected_career} ===")
                    recommendations = cluster_and_recommend(
                        df=df,
                        selected_career=selected_career,
                        n_recommendations=5,
                        use_cache=True
                    )
                    
                    print(f"Recommendations received: {recommendations}")
                    
                    if not recommendations:
                        st.warning("No recommendations were returned. Please try again or select a different career.")
                    elif isinstance(recommendations, list) and len(recommendations) > 0:
                        if any(isinstance(rec, str) and rec.startswith(('Error:', 'Error ')) for rec in recommendations):
                            # Handle error messages
                            for msg in recommendations:
                                if isinstance(msg, str) and msg.startswith(('Error:', 'Error ')):
                                    st.error(msg)
                        elif any(isinstance(rec, str) and rec.startswith('Selected career') for rec in recommendations):
                            # Handle warning messages
                            for msg in recommendations:
                                if isinstance(msg, str) and msg.startswith('Selected career'):
                                    st.warning(msg)
                        else:
                            # Display recommendations
                            display_career_recommendations(selected_career, recommendations)
                    else:
                        st.warning("No recommendations found for the selected career.")
                        
                except Exception as e:
                    error_msg = f"An unexpected error occurred: {str(e)}"
                    print(f"Error in main app: {error_msg}")
                    import traceback
                    print(traceback.format_exc())
                    st.error("An unexpected error occurred while processing your request. Please try again.")
                    
                    # Show additional career details if available with enhanced UI
                    career_mask = df['Career'] == selected_career
                    if career_mask.any():
                        career_details = df[career_mask].iloc[0]
                        
                        # Create an expander with custom styling
                        with st.expander(
                            label=f"<span style='color: #3498db;'><i class='fas fa-info-circle'></i> View Career Details</span>",
                            expanded=False
                        ):
                            st.markdown("""
                            <style>
                            .career-detail {
                                background-color: #2d3436;
                                border-radius: 8px;
                                padding: 15px;
                                margin-bottom: 15px;
                                border-left: 4px solid #3498db;
                            }
                            .career-detail h4 {
                                color: #3498db;
                                margin-top: 0;
                                margin-bottom: 10px;
                                font-size: 1.1em;
                            }
                            .career-detail p {
                                margin: 5px 0;
                                color: #ecf0f1;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # Domain section
                            st.markdown(f"""
                            <div class='career-detail'>
                                <h4><i class='fas fa-layer-group' style='margin-right: 8px;'></i>Domain</h4>
                                <p>{career_details.get('Domain', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Skills section
                            skills = career_details.get('Skills', 'N/A')
                            if skills != 'N/A':
                                skills_list = ", ".join([f"<span style='background-color: #3498db20; padding: 3px 8px; border-radius: 12px; margin: 2px; display: inline-block;'>{skill.strip()}</span>" 
                                                         for skill in str(skills).split(',') if skill.strip()])
                                st.markdown(f"""
                                <div class='career-detail'>
                                    <h4><i class='fas fa-tools' style='margin-right: 8px;'></i>Required Skills</h4>
                                    <div style='margin-top: 8px;'>{skills_list}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Exams section
                            if 'Exams' in df.columns and pd.notna(career_details.get('Exams')):
                                exams = career_details['Exams']
                                exams_list = ", ".join([f"<span style='background-color: #e74c3c20; padding: 3px 8px; border-radius: 12px; margin: 2px; display: inline-block;'>{exam.strip()}</span>" 
                                                      for exam in str(exams).split(',') if exam.strip()])
                                st.markdown(f"""
                                <div class='career-detail'>
                                    <h4><i class='fas fa-graduation-cap' style='margin-right: 8px;'></i>Common Exams</h4>
                                    <div style='margin-top: 8px;'>{exams_list}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Description section
                            description = career_details.get('Description', 'No description available.')
                            st.markdown(f"""
                            <div class='career-detail'>
                                <h4><i class='fas fa-align-left' style='margin-right: 8px;'></i>Description</h4>
                                <p style='line-height: 1.6;'>{description}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("No additional details available for this career.", icon="ℹ️")
                        
                except Exception as e:
                    st.error("An error occurred while generating recommendations.")
                    st.error("Please try the following:")
                    st.markdown("1. Try selecting a different career")
                    st.markdown("2. Refresh the page and try again")
                    st.markdown("3. Check the terminal for detailed error messages")
                    st.error(f"Technical details: {str(e)}")
        
    # Domain distribution visualization with modern dark theme
    st.markdown("---")
    
    # Section header with icon and gradient text
    st.markdown("""
    <div style='margin: 2rem 0 1.5rem 0;'>
        <h2 style='margin: 0; font-size: 1.8rem; background: linear-gradient(90deg, var(--primary), #8b5cf6); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>
            <i class='fas fa-chart-pie' style='margin-right: 12px;'></i>
            Career Insights & Analytics
        </h2>
        <div style='height: 4px; width: 80px; background: linear-gradient(90deg, var(--primary), #8b5cf6); 
                    margin: 0.5rem 0 1.5rem 0; border-radius: 2px;'></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "📊 Domain Distribution", 
        "📈 Career Comparison", 
        "🌐 Career Network"
    ])
    
    with tab1:
        st.markdown("### Career Distribution by Domain")
        
        # Create two columns for the charts
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            # Pie chart with modern styling
            domain_counts = df['Domain'].value_counts().reset_index()
            domain_counts.columns = ['Domain', 'Count']
            
            # Generate a color sequence based on the number of domains
            colors = px.colors.qualitative.Pastel[:len(domain_counts)]
            
            fig_pie = px.pie(
                domain_counts,
                names='Domain',
                values='Count',
                color_discrete_sequence=colors,
                hole=0.5,
                title=''
            )
            
            # Update pie chart layout for dark theme
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(color='white', size=11),
                marker=dict(line=dict(color='var(--bg-darker)', width=1.5)),
                hovertemplate="<b>%{label}</b><br>" +
                              "Count: %{value}<br>" +
                              "Percentage: %{percent}<extra></extra>",
                rotation=45
            )
            
            fig_pie.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='sans-serif'),
                margin=dict(t=0, b=0, l=0, r=0),
                height=400,
                hoverlabel=dict(
                    bgcolor='var(--card-bg)',
                    font_size=12,
                    font_family="sans-serif"
                )
            )
            
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Horizontal bar chart with modern styling
            domain_counts_sorted = domain_counts.sort_values('Count', ascending=True)
            
            fig_bar = px.bar(
                domain_counts_sorted,
                x='Count',
                y='Domain',
                orientation='h',
                color='Domain',
                color_discrete_sequence=colors,
                text='Count',
                title=''
            )
            
            # Update bar chart layout for dark theme
            fig_bar.update_traces(
                textposition='outside',
                textfont=dict(color='white', size=11),
                marker=dict(line=dict(color='var(--bg-darker)', width=1.5)),
                hovertemplate="<b>%{y}</b><br>" +
                              "Count: %{x}<extra></extra>"
            )
            
            fig_bar.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='sans-serif'),
                xaxis=dict(
                    showgrid=False,
                    title='Number of Careers',
                    title_font=dict(size=12, color='var(--text-secondary)'),
                    tickfont=dict(color='var(--text-secondary)'),
                    showline=True,
                    linecolor='var(--border-color)',
                    linewidth=1
                ),
                yaxis=dict(
                    showgrid=False,
                    title='',
                    tickfont=dict(color='var(--text-secondary)'),
                    showline=True,
                    linecolor='var(--border-color)',
                    linewidth=1
                ),
                margin=dict(t=0, b=0, l=0, r=0),
                height=400,
                hoverlabel=dict(
                    bgcolor='var(--card-bg)',
                    font_size=12,
                    font_family="sans-serif"
                )
            )
            
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        st.markdown("### Career Comparison by Domain")
        
        if 'Domain' in df.columns and 'Career' in df.columns:
            # Create a scatter plot with modern styling
            fig_scatter = px.scatter(
                df, 
                x='Domain', 
                y='Career', 
                color='Domain',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                labels={'Domain': 'Domain', 'Career': 'Career'},
                hover_name='Career',
                hover_data={'Domain': True, 'Career': False},
                title='',
                size_max=15
            )
            
            # Update scatter plot layout for dark theme
            fig_scatter.update_traces(
                marker=dict(
                    size=14,
                    opacity=0.8,
                    line=dict(width=1.5, color='var(--bg-darker)'),
                    symbol='circle'
                ),
                selector=dict(mode='markers'),
                hovertemplate="<b>%{hovertext}</b><br>" +
                              "Domain: %{x}<extra></extra>"
            )
            
            fig_scatter.update_layout(
                showlegend=True,
                legend=dict(
                    title='',
                    bgcolor='rgba(0,0,0,0)',
                    font=dict(color='var(--text-secondary)', size=12),
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='center',
                    x=0.5,
                    itemsizing='constant'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='sans-serif'),
                xaxis=dict(
                    showgrid=False,
                    title='Domain',
                    title_font=dict(size=12, color='var(--text-secondary)'),
                    tickfont=dict(color='var(--text-secondary)'),
                    showline=True,
                    linecolor='var(--border-color)',
                    linewidth=1,
                    tickangle=45
                ),
                yaxis=dict(
                    showgrid=False,
                    title='Career',
                    title_font=dict(size=12, color='var(--text-secondary)'),
                    tickfont=dict(color='var(--text-secondary)'),
                    showline=True,
                    linecolor='var(--border-color)',
                    linewidth=1
                ),
                margin=dict(t=20, b=80, l=80, r=20),
                height=600,
                hoverlabel=dict(
                    bgcolor='var(--card-bg)',
                    font_size=12,
                    font_family="sans-serif"
                ),
                transition_duration=300
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': True})
        else:
            st.warning("Required columns 'Domain' and 'Career' not found in the dataset.")
    
    with tab3:
        st.markdown("### Career Network Graph")
        
        # Placeholder for network graph visualization
        st.info("🔍 Network graph visualization is coming soon! This will show relationships between different careers based on skills and domains.", icon="ℹ️")
        
        # Add a placeholder image or text description
        st.markdown("""
        <div style='background: var(--card-bg); border-radius: 12px; padding: 2rem; text-align: center; 
                    border: 1px dashed var(--border-color); margin: 1rem 0;'>
            <i class='fas fa-project-diagram' style='font-size: 3rem; color: var(--primary); margin-bottom: 1rem;'></i>
            <h3 style='color: var(--text-primary); margin: 0.5rem 0;'>Interactive Career Network</h3>
            <p style='color: var(--text-secondary); margin: 0;'>
                Visualize how different careers are connected based on shared skills, 
                domains, and career progression paths.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add some statistics or key insights
        if 'Domain' in df.columns and 'Skills' in df.columns:
            st.markdown("#### Key Insights")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Careers", len(df))
            
            with col2:
                st.metric("Unique Domains", df['Domain'].nunique())
                
            with col3:
                # Count unique skills (approximate)
                all_skills = set()
                for skills in df['Skills'].dropna():
                    all_skills.update([s.strip() for s in str(skills).split(',')])
                st.metric("Unique Skills", len(all_skills))
            
            # Add a small multiple line chart showing skills distribution
            st.markdown("#### Skills Distribution by Domain")
            st.info("📊 This visualization will show the most common skills across different career domains.", icon="ℹ️")

if __name__ == "__main__":
    main()
