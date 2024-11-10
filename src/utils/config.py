import yaml
from pathlib import Path
from typing import Dict

def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}

# Default configuration
DEFAULT_CONFIG = {
    'theme': {
        'primary_color': '#1f77b4',
        'secondary_color': '#ff7f0e',
        'background_color': '#ffffff',
        'text_color': '#2c3e50',
        'font_family': 'Assistant, sans-serif'
    },
    'data': {
        'cache_dir': '.cache',
        'data_dir': 'data'
    },
    'api': {
        'twitter_api_key': '',
        'bring_them_home_api_key': '',  # If required
        'user_agent': 'SocialPulse/1.0 (Research Project)',
        'knesset_api_url': 'https://knesset.gov.il/api/v1'
    }
} 