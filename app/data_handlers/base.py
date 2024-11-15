from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataHandler(ABC):
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataframe columns"""
        try:
            # Standardize column names
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            
            # Essential columns with default values
            essential_columns = {
                'id': lambda x: range(len(x)),
                'name': 'Unknown',
                'age': -1,
                'location_taken': 'Unknown',
                'days_in_captivity': -1,
                'status': 'Unknown'
            }
            
            # Add missing columns with defaults
            for col, default in essential_columns.items():
                if col not in df.columns:
                    df[col] = default(df) if callable(default) else default
            
            # Clean specific columns
            if 'age' in df.columns:
                df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(-1)
            
            if 'days_in_captivity' in df.columns:
                df['days_in_captivity'] = pd.to_numeric(df['days_in_captivity'], errors='coerce').fillna(-1)
            
            return df
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            return pd.DataFrame()

    @abstractmethod
    def read_data(self, **kwargs) -> pd.DataFrame:
        pass 