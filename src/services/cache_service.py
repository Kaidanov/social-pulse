import os
import pandas as pd
from datetime import datetime, timedelta
import json

class CacheService:
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        self.cache_duration = timedelta(hours=1)
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_cached_data(self, key: str) -> pd.DataFrame:
        """Get data from cache if it exists and is not expired"""
        cache_path = os.path.join(self.cache_dir, f"{key}.csv")
        meta_path = os.path.join(self.cache_dir, f"{key}_meta.json")
        
        if not (os.path.exists(cache_path) and os.path.exists(meta_path)):
            return None
            
        # Check if cache is expired
        with open(meta_path, 'r') as f:
            meta = json.load(f)
            cached_time = datetime.fromisoformat(meta['timestamp'])
            if datetime.now() - cached_time > self.cache_duration:
                return None
        
        return pd.read_csv(cache_path)
        
    def cache_data(self, key: str, data: pd.DataFrame):
        """Cache data with metadata"""
        if data is None or data.empty:
            return
            
        cache_path = os.path.join(self.cache_dir, f"{key}.csv")
        meta_path = os.path.join(self.cache_dir, f"{key}_meta.json")
        
        # Save data
        data.to_csv(cache_path, index=False)
        
        # Save metadata
        meta = {
            'timestamp': datetime.now().isoformat(),
            'rows': len(data),
            'columns': list(data.columns)
        }
        with open(meta_path, 'w') as f:
            json.dump(meta, f) 