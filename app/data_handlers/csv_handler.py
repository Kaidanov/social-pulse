import pandas as pd
import os
from typing import List
import logging
from .base import DataHandler

logger = logging.getLogger(__name__)

class CSVHandler(DataHandler):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
    def get_available_files(self) -> List[str]:
        """Get list of available CSV files"""
        try:
            return [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
        except Exception as e:
            logger.error(f"Error listing CSV files: {str(e)}")
            return []
    
    def read_data(self, filename: str) -> pd.DataFrame:
        """Read and clean CSV data"""
        try:
            file_path = os.path.join(self.data_dir, filename)
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return pd.DataFrame()
                
            df = pd.read_csv(file_path)
            return self.clean_data(df)
        except Exception as e:
            logger.error(f"Error reading CSV {filename}: {str(e)}")
            return pd.DataFrame() 