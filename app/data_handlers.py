import pandas as pd
import json
import requests
from typing import Dict, List, Optional
import os
from datetime import datetime

class DataSourceHandler:
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataframe columns"""
        # Standardize column names
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # Essential columns with default values
        essential_columns = {
            'id': lambda: range(len(df)),
            'name': 'Unknown',
            'age': -1,
            'location_taken': 'Unknown',
            'days_in_captivity': -1
        }
        
        # Add missing columns with defaults
        for col, default in essential_columns.items():
            if col not in df.columns:
                df[col] = default() if callable(default) else default
        
        # Clean specific columns
        if 'age' in df.columns:
            df['age'] = pd.to_numeric(df['age'], errors='coerce').fillna(-1)
        
        if 'days_in_captivity' in df.columns:
            df['days_in_captivity'] = pd.to_numeric(df['days_in_captivity'], errors='coerce').fillna(-1)
        
        return df

class CSVHandler(DataSourceHandler):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
    def get_available_files(self) -> List[str]:
        """Get list of available CSV files"""
        return [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
    
    def read_data(self, filename: str) -> pd.DataFrame:
        """Read and clean CSV data"""
        try:
            df = pd.read_csv(os.path.join(self.data_dir, filename))
            return self.clean_data(df)
        except Exception as e:
            print(f"Error reading CSV {filename}: {str(e)}")
            return pd.DataFrame()

class APIHandler(DataSourceHandler):
    def __init__(self, api_url: Optional[str] = None):
        self.api_url = api_url or "https://api.example.com/hostages"
        
    def read_data(self) -> pd.DataFrame:
        """Read and clean API data"""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            return self.clean_data(df)
        except Exception as e:
            print(f"Error reading from API: {str(e)}")
            return pd.DataFrame()

class DatabaseHandler(DataSourceHandler):
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string
        
    def read_data(self) -> pd.DataFrame:
        """Read and clean database data"""
        try:
            # Implement database connection and query
            # This is a placeholder - implement actual database connection
            df = pd.DataFrame()  # Replace with actual database query
            return self.clean_data(df)
        except Exception as e:
            print(f"Error reading from database: {str(e)}")
            return pd.DataFrame() 