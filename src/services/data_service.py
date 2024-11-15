import pandas as pd
import os
from datetime import datetime
from typing import Dict, List
from src.data.data_sources import IDFDataSource
import streamlit as st
from src.core.models import Hostage

class DataService:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.idf_source = IDFDataSource()
        os.makedirs(data_dir, exist_ok=True)

    def load_hostages(self) -> pd.DataFrame:
        """Load hostages dataset from IDF source and cache"""
        return self._load_hostages_cached()

    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def _load_hostages_cached(_self) -> pd.DataFrame:  # Note the _self parameter
        try:
            df = _self.idf_source.fetch_data()
            if df is None or df.empty:
                st.warning("No data received from source")
                return pd.DataFrame()
            
            return df
        except Exception as e:
            st.error(f"Error loading hostages data: {str(e)}")
            return pd.DataFrame()

    def get_hostages_summary(self) -> Dict:
        """Get summary statistics of hostages"""
        try:
            df = self._load_hostages_cached()  # Use cached method
            if df.empty:
                return {
                    'total': 0,
                    'released': 0,
                    'held': 0,
                    'deceased': 0
                }
            
            # Convert status to lowercase for consistent comparison
            df['status'] = df['status'].str.lower()
            
            return {
                'total': len(df),
                'released': len(df[df['status'] == 'released']),
                'held': len(df[df['status'] == 'held']),
                'deceased': len(df[df['status'] == 'deceased'])
            }
        except Exception as e:
            st.error(f"Error getting hostages summary: {e}")
            return {
                'total': 0,
                'released': 0,
                'held': 0,
                'deceased': 0
            }

    @st.cache_data(ttl=3600)
    def get_age_statistics(_self) -> Dict:  # Note the _self parameter
        """Get detailed age statistics"""
        try:
            df = _self._load_hostages_cached()
            if df.empty or 'age' not in df.columns:
                return {
                    'average_age': 0,
                    'median_age': 0,
                    'min_age': 0,
                    'max_age': 0
                }
            
            # Convert age to numeric, handling any non-numeric values
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
            
            return {
                'average_age': df['age'].mean(),
                'median_age': df['age'].median(),
                'min_age': df['age'].min(),
                'max_age': df['age'].max()
            }
        except Exception as e:
            st.error(f"Error getting age statistics: {e}")
            return {
                'average_age': 0,
                'median_age': 0,
                'min_age': 0,
                'max_age': 0
            }

    @st.cache_data(ttl=3600)
    def get_latest_updates(_self, n: int = 5) -> List[Dict]:  # Note the _self parameter
        """Get latest hostage updates"""
        try:
            df = _self._load_hostages_cached()
            if df.empty:
                return []
            
            # Ensure capture_date is datetime
            df['capture_date'] = pd.to_datetime(df['capture_date'], errors='coerce')
            
            # Sort by capture date and get latest updates
            df = df.sort_values('capture_date', ascending=False)
            latest = df.head(n)
            
            updates = []
            for _, row in latest.iterrows():
                updates.append({
                    'date': row.get('capture_date', '').strftime('%Y-%m-%d') if pd.notnull(row.get('capture_date')) else '',
                    'title': f"Update for {row.get('name', 'Unknown')}",
                    'content': row.get('details', ''),
                    'source': 'IDF',
                    'link': '#',
                    'excerpt': row.get('details', '')[:200] + '...' if row.get('details') else ''
                })
            
            return updates
        except Exception as e:
            st.error(f"Error getting latest updates: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get all statistics in one call"""
        try:
            return {
                'summary': self.get_hostages_summary(),
                'age_stats': self.get_age_statistics(),
                'latest_updates': self.get_latest_updates()
            }
        except Exception as e:
            st.error(f"Error getting statistics: {e}")
            return {
                'summary': {},
                'age_stats': {},
                'latest_updates': []
            }