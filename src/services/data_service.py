import pandas as pd
import os
from datetime import datetime
from typing import Dict, List
from src.data.data_sources import IDFDataSource

class DataService:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.idf_source = IDFDataSource()
        os.makedirs(data_dir, exist_ok=True)

    def load_hostages(self) -> pd.DataFrame:
        """Load hostages dataset from IDF source and cache"""
        try:
            # Try to get fresh data from IDF
            df = self.idf_source.fetch_data()
            
            # Cache the data if successful
            if not df.empty:
                cache_path = os.path.join(self.data_dir, 'hostages_cache.csv')
                df.to_csv(cache_path, index=False)
                return df
            
            # If fetch failed, try to load from cache
            cache_path = os.path.join(self.data_dir, 'hostages_cache.csv')
            if os.path.exists(cache_path):
                return pd.read_csv(cache_path)
                
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error loading hostages data: {e}")
            return pd.DataFrame()

    def get_hostages_summary(self) -> Dict:
        """Get summary statistics of hostages"""
        df = self.load_hostages()
        if df.empty:
            return {
                'total': 0,
                'released': 0,
                'held': 0,
                'deceased': 0
            }
        
        return {
            'total': len(df),
            'released': len(df[df['status'].str.lower() == 'released']) if 'status' in df.columns else 0,
            'held': len(df[df['status'].str.lower() == 'held']) if 'status' in df.columns else 0,
            'deceased': len(df[df['status'].str.lower() == 'deceased']) if 'status' in df.columns else 0
        }

    def get_age_statistics(self) -> Dict:
        """Get detailed age statistics"""
        df = self.load_hostages()
        if df.empty or 'age' not in df.columns:
            return {
                'average_age': 0,
                'median_age': 0,
                'min_age': 0,
                'max_age': 0
            }
        
        return {
            'average_age': df['age'].mean(),
            'median_age': df['age'].median(),
            'min_age': df['age'].min(),
            'max_age': df['age'].max()
        }

    def get_latest_updates(self, n: int = 5) -> List[Dict]:
        """Get latest hostage updates"""
        df = self.load_hostages()
        if df.empty:
            return []
        
        # Sort by capture date and get latest updates
        df = df.sort_values('capture_date', ascending=False)
        latest = df.head(n)
        
        updates = []
        for _, row in latest.iterrows():
            updates.append({
                'date': row.get('capture_date', ''),
                'title': f"Update for {row.get('name', 'Unknown')}",
                'content': row.get('details', ''),
                'source': 'IDF',
                'link': '#',
                'excerpt': row.get('details', '')[:200] + '...' if row.get('details') else ''
            })
        
        return updates

    def get_statistics(self) -> Dict:
        """Get all statistics in one call"""
        return {
            'summary': self.get_hostages_summary(),
            'age_stats': self.get_age_statistics(),
            'latest_updates': self.get_latest_updates()
        }