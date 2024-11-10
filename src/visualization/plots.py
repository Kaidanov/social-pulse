import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def create_time_series(df: pd.DataFrame) -> go.Figure:
    """Create time series visualization based on data type"""
    try:
        if 'text' in df.columns:  # Social media data
            daily_engagement = df.groupby('date').agg({
                'likes': 'sum',
                'retweets': 'sum'
            }).reset_index()
            
            fig = px.line(daily_engagement, x='date', 
                         y=['likes', 'retweets'],
                         title='Social Media Engagement Over Time',
                         labels={'value': 'Count', 'date': 'Date', 
                                'variable': 'Metric'})
        else:  # Hostage data
            if 'תאריך_חטיפה' not in df.columns:
                return None
                
            daily_counts = df.groupby(['תאריך_חטיפה', 'סטטוס']).size().unstack(fill_value=0)
            fig = px.line(daily_counts, 
                         title='Hostages Timeline by Status',
                         labels={'value': 'Count', 'תאריך_חטיפה': 'Date'})
        
        fig.update_layout(
            title_x=0.5,
            title_font=dict(size=20),
            font=dict(size=14)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating time series: {str(e)}")
        return None

def create_category_distribution(df: pd.DataFrame) -> go.Figure:
    """Create distribution visualization based on data type"""
    try:
        if 'text' in df.columns:  # Social media data
            engagement_bins = pd.cut(df['likes'] + df['retweets'], 
                                   bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
            counts = engagement_bins.value_counts()
            
            fig = px.pie(values=counts.values, 
                        names=counts.index,
                        title='Engagement Distribution')
        else:  # Hostage data
            if 'סטטוס' not in df.columns:
                return None
                
            status_counts = df['סטטוס'].value_counts()
            fig = px.pie(values=status_counts.values, 
                        names=status_counts.index,
                        title='Status Distribution')
        
        fig.update_layout(
            title_x=0.5,
            title_font=dict(size=20),
            font=dict(size=14)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating distribution: {str(e)}")
        return None

def create_age_distribution(df: pd.DataFrame) -> go.Figure:
    """Create age distribution visualization"""
    try:
        if 'קבוצת_גיל' not in df.columns:
            return None
            
        age_counts = df['קבוצת_גיל'].value_counts()
        fig = px.bar(x=age_counts.index, 
                     y=age_counts.values,
                     title='Age Group Distribution',
                     labels={'x': 'Age Group', 'y': 'Count'})
        
        fig.update_layout(
            title_x=0.5,
            title_font=dict(size=20),
            font=dict(size=14)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating age distribution: {str(e)}")
        return None

def create_social_metrics(df: pd.DataFrame) -> go.Figure:
    """Create social media metrics visualization"""
    try:
        if 'text' not in df.columns:
            return None
            
        # Calculate engagement metrics
        df['total_engagement'] = df['likes'] + df['retweets']
        df['hour'] = pd.to_datetime(df['date']).dt.hour
        
        hourly_metrics = df.groupby('hour').agg({
            'likes': 'mean',
            'retweets': 'mean',
            'total_engagement': 'mean'
        }).round(2)
        
        fig = px.line(hourly_metrics, 
                     title='Average Engagement by Hour',
                     labels={'value': 'Average Count', 'hour': 'Hour of Day'})
        
        fig.update_layout(
            title_x=0.5,
            title_font=dict(size=20),
            font=dict(size=14)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating social metrics: {str(e)}")
        return None