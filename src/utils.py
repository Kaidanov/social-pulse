import streamlit as st
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
import yaml

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="SocialPulse | סושיאל-פולס",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def setup_rtl_support():
    """Add RTL support for Hebrew"""
    rtl_css = """
        <style>
        .rtl {
            direction: rtl;
            text-align: right;
        }
        .stMarkdown, .stText {
            text-align: right;
        }
        .st-emotion-cache-1y4p8pa {
            direction: rtl;
        }
        .st-emotion-cache-16idsys p {
            text-align: right;
        }
        </style>
    """
    st.markdown(rtl_css, unsafe_allow_html=True)

def show_error(message):
    """Display error message in Hebrew/English"""
    st.error(f"🚫 {message}")

def show_success(message):
    """Display success message in Hebrew/English"""
    st.success(f"✅ {message}")

def show_info(message):
    """Display info message in Hebrew/English"""
    st.info(f"ℹ️ {message}")

def load_config(config_path: str = "config.yaml"):
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        show_error(f"Error loading config: {str(e)}")
        return {}

def format_date(date_str: str) -> datetime:
    """Format date string to datetime object with Hebrew support"""
    try:
        return pd.to_datetime(date_str)
    except Exception as e:
        show_error(f"Error formatting date: {str(e)}")
        return None

def export_to_csv(df: pd.DataFrame, filename: str):
    """Export DataFrame to CSV with proper encoding"""
    try:
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return True
    except Exception as e:
        show_error(f"Error exporting to CSV: {str(e)}")
        return False

def cache_data(key: str, data: any, cache_dir: str = ".cache"):
    """Cache data to file"""
    try:
        Path(cache_dir).mkdir(exist_ok=True)
        cache_path = Path(cache_dir) / f"{key}.json"
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        return True
    except Exception as e:
        show_error(f"Error caching data: {str(e)}")
        return False

def load_cached_data(key: str, cache_dir: str = ".cache"):
    """Load data from cache"""
    try:
        cache_path = Path(cache_dir) / f"{key}.json"
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        show_error(f"Error loading cached data: {str(e)}")
    return None

def validate_dataframe(df: pd.DataFrame, required_columns: list) -> bool:
    """Validate DataFrame structure"""
    if df is None:
        show_error("No data provided")
        return False
    
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        show_error(f"Missing required columns: {', '.join(missing_cols)}")
        return False
    
    return True

def setup_logging():
    """Configure logging with Hebrew support"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('SocialPulse')

# Theme configuration
THEME = {
    'primary_color': '#1f77b4',
    'secondary_color': '#ff7f0e',
    'background_color': '#ffffff',
    'text_color': '#2c3e50',
    'font_family': 'Assistant, sans-serif'
}

# Error messages in Hebrew and English
ERROR_MESSAGES = {
    'no_data': {
        'he': 'לא נמצאו נתונים',
        'en': 'No data found'
    },
    'invalid_date': {
        'he': 'תאריך לא תקין',
        'en': 'Invalid date'
    },
    'file_error': {
        'he': 'שגיאה בטעינת הקובץ',
        'en': 'File loading error'
    }
} 