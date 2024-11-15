from dataclasses import dataclass
from typing import Dict, Any
import os
from dotenv import load_dotenv

@dataclass
class Config:
    """Application configuration"""
    DATA_DIR: str = "data"
    CACHE_DIR: str = "data/cache"
    
    # API URLs
    IDF_URL: str = "https://www.idf.il/en/minisites/news-feed/"
    MFA_URL: str = "https://www.gov.il/en/departments/news"
    
    # Cache settings
    CACHE_EXPIRY: int = 3600  # 1 hour
    
    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from environment variables"""
        load_dotenv()
        return cls(
            DATA_DIR=os.getenv('DATA_DIR', 'data'),
            CACHE_DIR=os.getenv('CACHE_DIR', 'data/cache'),
            IDF_URL=os.getenv('IDF_URL', cls.IDF_URL),
            MFA_URL=os.getenv('MFA_URL', cls.MFA_URL),
            CACHE_EXPIRY=int(os.getenv('CACHE_EXPIRY', cls.CACHE_EXPIRY))
        ) 