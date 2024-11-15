from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class Config:
    DATA_DIR: str = "data"
    CACHE_DIR: str = "data/cache"
    API_KEY: str = os.getenv('GOV_IL_API_KEY', '')
    API_BASE_URL: str = "https://data.gov.il/api/3/action/"
    
    @classmethod
    def load(cls) -> 'Config':
        """Load configuration"""
        load_dotenv()  # Load environment variables
        return cls(
            DATA_DIR=os.getenv('DATA_DIR', 'data'),
            CACHE_DIR=os.getenv('CACHE_DIR', 'data/cache'),
            API_KEY=os.getenv('GOV_IL_API_KEY', ''),
            API_BASE_URL=os.getenv('API_BASE_URL', "https://data.gov.il/api/3/action/")
        ) 