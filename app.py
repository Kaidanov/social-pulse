import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import os
import json

class DataSources:
    def __init__(self):
        self.cache_dir = 'data'
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def fetch_idf_blog(self):
        """Fetch IDF blog updates"""
        try:
            url = "https://www.idf.il/en/articles/news/"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            updates = []
            
            for item in soup.select('.article-item'):
                updates.append({
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'title': item.select_one('h2').text.strip() if item.select_one('h2') else '',
                    'content': item.select_one('p').text.strip() if item.select_one('p') else '',
                    'source': 'IDF Blog'
                })
            return pd.DataFrame(updates)
        except Exception as e:
            st.error(f"Error fetching IDF blog: {str(e)}")
            return pd.DataFrame()

    def fetch_mfa_updates(self):
        """Fetch Ministry of Foreign Affairs updates"""
        try:
            url = "https://www.gov.il/en/departments/news/ministry-of-foreign-affairs-news"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            updates = []
            
            for item in soup.select('.news-item'):
                updates.append({
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'title': item.select_one('h3').text.strip() if item.select_one('h3') else '',
                    'content': item.select_one('.content').text.strip() if item.select_one('.content') else '',
                    'source': 'MFA Updates'
                })
            return pd.DataFrame(updates)
        except Exception as e:
            st.error(f"Error fetching MFA updates: {str(e)}")
            return pd.DataFrame()

    def fetch_hostages_data(self):
        """Load and process hostages data"""
        try:
            df = pd.read_csv('data/hostages.csv')
            # Add data processing if needed
            return df
        except Exception as e:
            st.error(f"Error loading hostages data: {str(e)}")
            return pd.DataFrame()

class DataManager:
    def __init__(self):
        self.cache_dir = 'data'
        self.data_sources = DataSources()
        self.ensure_cache_dir()
        
    def ensure_cache_dir(self):
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def refresh_data(self):
        """Fetch and combine data from all sources"""
        # Fetch data from each source
        idf_updates = self.data_sources.fetch_idf_blog()
        mfa_updates = self.data_sources.fetch_mfa_updates()
        hostages_data = self.data_sources.fetch_hostages_data()
        
        # Save updated data
        if not idf_updates.empty:
            self.save_data(idf_updates, 'idf_updates.csv')
        if not mfa_updates.empty:
            self.save_data(mfa_updates, 'mfa_updates.csv')
        if not hostages_data.empty:
            self.save_data(hostages_data, 'hostages.csv')
        
        return {
            'idf_updates': idf_updates,
            'mfa_updates': mfa_updates,
            'hostages_data': hostages_data
        }

    def load_cached_data(self, filename):
        try:
            file_path = os.path.join(self.cache_dir, filename)
            if os.path.exists(file_path):
                return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

    def save_data(self, df, filename):
        try:
            file_path = os.path.join(self.cache_dir, filename)
            df.to_csv(file_path, index=False)
        except Exception as e:
            st.error(f"Error saving data: {str(e)}")

def create_age_distribution_chart(df):
    """Create an enhanced age distribution visualization"""
    if 'age' not in df.columns:
        return None
    
    fig = px.histogram(
        df,
        x='age',
        nbins=20,
        title='Age Distribution of Hostages',
        labels={'age': 'Age', 'count': 'Number of People'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=40, l=0, r=0, b=0)
    )
    return fig

def create_status_timeline(df):
    """Create a timeline of status changes"""
    if 'status' not in df.columns or 'date' not in df.columns:
        return None
    
    fig = px.line(
        df.groupby(['date', 'status']).size().reset_index(name='count'),
        x='date',
        y='count',
        color='status',
        title='Status Changes Over Time',
        labels={'date': 'Date', 'count': 'Number of People', 'status': 'Status'}
    )
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig

def create_location_map(df):
    """Create a map visualization of locations"""
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        return None
    
    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='name',
        hover_data=['age', 'status'],
        zoom=7,
        title='Hostage Locations'
    )
    fig.update_layout(mapbox_style='carto-positron')
    return fig

# Add this new function for the sidebar menu
def create_sidebar_menu():
    st.sidebar.markdown("""
    <style>
        .sidebar-menu {
            padding: 0;
            margin: 0;
            list-style-type: none;
        }
        .sidebar-menu li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #2c3e50;
        }
        .sidebar-menu li:hover {
            background-color: #2c3e50;
            cursor: pointer;
        }
        .menu-header {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 1rem 0;
            color: #ecf0f1;
        }
        .user-profile {
            padding: 1rem;
            text-align: center;
            border-bottom: 1px solid #2c3e50;
        }
        .user-profile img {
            border-radius: 50%;
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # User Profile Section
    st.sidebar.markdown("""
        <div class="user-profile">
            <img src="https://via.placeholder.com/80" alt="User Profile"/>
            <h4 style="color: #ecf0f1;">John David</h4>
            <p style="color: #bdc3c7;">Administrator</p>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    menu_items = {
        "General": {
            "Dashboard": "📊",
            "Widgets": "🔧",
            "Elements": "🧩",
            "Tables": "📋"
        },
        "Data Sources": {
            "IDF Updates": "🔄",
            "MFA Updates": "📰",
            "Hostages Data": "👥",
            "News Feed": "📑"
        },
        "Analytics": {
            "Charts": "📈",
            "Reports": "📋",
            "Statistics": "📊"
        },
        "Settings": {
            "Profile": "👤",
            "Configuration": "⚙️",
            "Help": "❓"
        }
    }

    selected_section = None
    selected_item = None

    for section, items in menu_items.items():
        st.sidebar.markdown(f"<p class='menu-header'>{section}</p>", unsafe_allow_html=True)
        for item, icon in items.items():
            if st.sidebar.button(f"{icon} {item}", key=f"{section}-{item}"):
                selected_section = section
                selected_item = item

    return selected_section, selected_item

def main():
    st.set_page_config(
        page_title="Hostages Data Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for dark theme sidebar
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #1a2634;
            padding: 1rem;
        }
        .st-emotion-cache-1cypcdb {
            background-color: #1a2634;
        }
        .st-emotion-cache-1cypcdb:hover {
            background-color: #2c3e50;
        }
        .stButton>button {
            width: 100%;
            text-align: left;
            background-color: transparent;
            color: #ecf0f1;
            border: none;
            padding: 0.5rem;
        }
        .stButton>button:hover {
            background-color: #2c3e50;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create sidebar menu and get selected items
    selected_section, selected_item = create_sidebar_menu()

    # Rest of your existing main content code...
    data_manager = DataManager()

    # Main Content Header
    st.markdown('<p class="main-header">Hostages Data Dashboard</p>', unsafe_allow_html=True)

    # Show different content based on selection
    if selected_section and selected_item:
        st.subheader(f"{selected_section} > {selected_item}")
        
        if selected_item == "Dashboard":
            # Your existing dashboard content
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Total Hostages", "239", delta="-4")
                st.markdown('</div>', unsafe_allow_html=True)
            # ... (rest of your metrics)

        elif selected_item == "Charts":
            # Load and display charts
            hostages_df = data_manager.load_cached_data('hostages.csv')
            if not hostages_df.empty:
                tab1, tab2, tab3 = st.tabs(["Age Distribution", "Status Timeline", "Location Map"])
                # ... (your existing charts code)

        elif selected_item == "Reports":
            st.write("Reports section - Coming soon")

    else:
        # Show default dashboard content
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Total Hostages", "239", delta="-4")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Released", "110", delta="+4")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Still Held", "129", delta="-4")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.metric("Deceased", "11", delta="+0")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display charts
        hostages_df = data_manager.load_cached_data('hostages.csv')
        if not hostages_df.empty:
            tab1, tab2, tab3 = st.tabs(["Age Distribution", "Status Timeline", "Location Map"])
            
            with tab1:
                fig = create_age_distribution_chart(hostages_df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                fig = create_status_timeline(hostages_df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                fig = create_location_map(hostages_df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()