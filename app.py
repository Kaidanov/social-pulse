import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from src.data.data_processor import DataProcessor
from src.visualization.plots import (create_time_series, create_category_distribution,
                                   create_scatter_plot)
from src.utils.helpers import set_page_config, setup_rtl_support, show_error, show_success
from src.data.data_loader import IsraeliCrisisDataLoader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize data loader with config
config = {
    'twitter_api_key': os.getenv('TWITTER_BEARER_TOKEN'),
    'cache_dir': '.cache',
    'data_dir': 'data'
}

def display_data_overview(df):
    """Display overview metrics for the loaded data"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("סך הכל רשומות", f"{len(df):,}")
    
    with col2:
        st.metric("טווח תאריכים", 
                 f"{df['תאריך_חטיפה'].min().strftime('%d/%m/%y')} - {df['תאריך_חטיפה'].max().strftime('%d/%m/%y')}")
    
    with col3:
        status_counts = df['סטטוס'].value_counts()
        st.metric("בשבי", f"{status_counts.get('בשבי', 0):,}")
    
    with col4:
        st.metric("שוחררו", f"{status_counts.get('שוחרר', 0):,}")

def create_status_pie_chart(df):
    """Create pie chart for hostage status distribution"""
    status_counts = df['סטטוס'].value_counts()
    fig = px.pie(values=status_counts.values, 
                 names=status_counts.index,
                 title='התפלגות סטטוס חטופים')
    fig.update_layout(
        title_x=0.5,
        title_font=dict(size=20),
        font=dict(size=14)
    )
    return fig

def create_age_group_bar(df):
    """Create bar chart for age group distribution"""
    age_counts = df['קבוצת_גיל'].value_counts()
    fig = px.bar(x=age_counts.index, 
                 y=age_counts.values,
                 title='התפלגות קבוצות גיל',
                 labels={'x': 'קבוצת גיל', 'y': 'מספר חטופים'})
    fig.update_layout(
        title_x=0.5,
        title_font=dict(size=20),
        font=dict(size=14)
    )
    return fig

def main():
    # Initialize page config and RTL support
    set_page_config()
    setup_rtl_support()
    
    # Initialize session state
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = IsraeliCrisisDataLoader(config)
    
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    
    # Sidebar controls
    st.sidebar.title("בקרים")
    
    # Data source selector
    data_source = st.sidebar.selectbox(
        "בחר מקור נתונים",
        ["נתוני דוגמה", "נתונים רשמיים", "רשתות חברתיות"]
    )

    # Handle data loading based on source
    if data_source == "נתוני דוגמה":
        if st.sidebar.button("יצירת נתוני דוגמה"):
            st.session_state.current_data = st.session_state.data_loader.generate_sample_hostages_data()
            show_success("נתוני דוגמה נוצרו בהצלחה!")
    
    elif data_source == "נתונים רשמיים":
        if st.sidebar.button("טעינת נתונים רשמיים"):
            st.session_state.current_data = st.session_state.data_loader.load_hostages_data_from_gov()
            show_success("הנתונים נטענו בהצלחה!")
    
    elif data_source == "רשתות חברתיות":
        query = st.sidebar.text_input("חיפוש", value="#BringThemHomeNow")
        if st.sidebar.button("טעינת נתוני רשתות חברתיות"):
            st.session_state.current_data = st.session_state.data_loader.fetch_x_data(query=query)
            show_success("נתוני רשתות חברתיות נטענו בהצלחה!")

    # Main content area
    if st.session_state.current_data is not None:
        df = st.session_state.current_data
        
        # Display data overview
        st.header("סקירת נתונים")
        display_data_overview(df)
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs([
            "התפלגות סטטוס", 
            "התפלגות גיל",
            "נתונים לאורך זמן",
            "נתונים גולמיים"
        ])
        
        with tab1:
            st.plotly_chart(create_status_pie_chart(df), use_container_width=True)
            
        with tab2:
            st.plotly_chart(create_age_group_bar(df), use_container_width=True)
            
        with tab3:
            # Time series of hostages by status
            daily_counts = df.groupby(['תאריך_חטיפה', 'סטטוס']).size().unstack(fill_value=0)
            fig = px.line(daily_counts, 
                         title='מספר חטופים לאורך זמן לפי סטטוס',
                         labels={'value': 'מספר חטופים', 'תאריך_חטיפה': 'תאריך'})
            st.plotly_chart(fig, use_container_width=True)
            
        with tab4:
            st.dataframe(df, use_container_width=True)
    
    else:
        st.info("אנא בחר מקור נתונים וטען את הנתונים כדי להתחיל בניתוח.")

if __name__ == "__main__":
    main()