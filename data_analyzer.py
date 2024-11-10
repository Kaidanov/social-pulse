import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataAnalyzer:
    def __init__(self):
        self.data = None
        
    def load_data(self, file):
        """Load data from uploaded file"""
        try:
            self.data = pd.read_csv(file)
            # Convert date columns to datetime
            date_columns = self.data.select_dtypes(include=['object']).columns
            for col in date_columns:
                try:
                    self.data[col] = pd.to_datetime(self.data[col])
                except:
                    continue
            return True
        except Exception as e:
            return str(e)
    
    def generate_sample_data(self, rows=1000):
        """Generate sample data for demonstration"""
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=365),
            end=datetime.now(),
            periods=rows
        )
        
        categories = ['A', 'B', 'C', 'D']
        
        self.data = pd.DataFrame({
            'date': dates,
            'value': np.random.normal(100, 15, rows),
            'category': np.random.choice(categories, rows),
            'quantity': np.random.randint(1, 100, rows)
        })
        return self.data
    
    def get_summary_stats(self):
        """Calculate summary statistics"""
        if self.data is None:
            return None
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        return self.data[numeric_cols].describe()
    
    def filter_data(self, start_date=None, end_date=None, category=None):
        """Filter data based on date range and category"""
        if self.data is None:
            return None
            
        filtered_data = self.data.copy()
        
        if start_date and 'date' in filtered_data.columns:
            start_datetime = pd.to_datetime(start_date)
            filtered_data = filtered_data[filtered_data['date'] >= start_datetime]
            
        if end_date and 'date' in filtered_data.columns:
            end_datetime = pd.to_datetime(end_date)
            filtered_data = filtered_data[filtered_data['date'] <= end_datetime]
            
        if category and 'category' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['category'] == category]
            
        return filtered_data 