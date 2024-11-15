import streamlit as st
import os
from src.ui.components import SidebarMenu
from src.services.chart_service import ChartService
from src.services.data_service import DataService
from src.core.config import Config
from typing import List, Dict

def initialize_services(config: Config):
    """Initialize all services with configuration"""
    # Initialize services
    data_service = DataService(config.DATA_DIR)
    chart_service = ChartService()
    sidebar_menu = SidebarMenu()
    
    return {
        'data_service': data_service,
        'chart_service': chart_service,
        'sidebar_menu': sidebar_menu
    }

def render_latest_updates(updates: List[Dict]):
    """Render latest updates with enhanced styling"""
    st.markdown("""
        <style>
        .update-card {
            background: white;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .update-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .update-title {
            color: #1f77b4;
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-decoration: none;
        }
        .update-title:hover {
            color: #2c3e50;
        }
        .update-meta {
            font-size: 0.8rem;
            color: #666;
            margin-bottom: 0.5rem;
        }
        .update-excerpt {
            font-size: 0.9rem;
            color: #444;
            margin-bottom: 0.5rem;
        }
        .read-more {
            color: #1f77b4;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
        }
        .read-more:hover {
            text-decoration: underline;
        }
        .source-badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 1rem;
            font-size: 0.8rem;
            font-weight: 500;
            background: rgba(31, 119, 180, 0.1);
            color: #1f77b4;
        }
        </style>
    """, unsafe_allow_html=True)

    for update in updates:
        st.markdown(f"""
            <div class="update-card">
                <a href="{update['link']}" target="_blank" class="update-title">
                    {update['title']}
                </a>
                <div class="update-meta">
                    {update['date']} · <span class="source-badge">{update['source']}</span>
                </div>
                <div class="update-excerpt">
                    {update['excerpt']}
                </div>
                <a href="{update['link']}" target="_blank" class="read-more">
                    Read more →
                </a>
            </div>
        """, unsafe_allow_html=True)

def render_default_dashboard(services: dict):
    """Render the default dashboard view"""
    st.markdown("""
        <div class="main-content">
            <div class="dashboard-container">
                <h1 class="main-header">Hostages Data Dashboard</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Get data summaries
    data_service = services['data_service']
    hostages_summary = data_service.get_hostages_summary()
    
    # Display loading state
    with st.spinner("Loading data..."):
        hostages_data = data_service.load_hostages()
        
        if hostages_data.empty:
            st.warning("No hostage data available. Please check the data source connection.")
            return
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Hostages", hostages_summary['total'])
    with col2:
        st.metric("Released", hostages_summary['released'])
    with col3:
        st.metric("Still Held", hostages_summary['held'])
    with col4:
        st.metric("Deceased", hostages_summary['deceased'])
    
    # Display charts if data is available
    if not hostages_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Age Distribution")
            age_chart = services['chart_service'].create_chart(hostages_data, "age_distribution")
            if age_chart:
                st.plotly_chart(age_chart, use_container_width=True)
        
        with col2:
            st.subheader("Status Distribution")
            status_chart = services['chart_service'].create_chart(hostages_data, "status_pie")
            if status_chart:
                st.plotly_chart(status_chart, use_container_width=True)

def render_selected_content(section: str, item: str, services: dict):
    """Render content based on menu selection"""
    st.title(f"{section} - {item}")
    
    if section == "Dashboard":
        if item == "Overview":
            render_default_dashboard(services)
        elif item == "Analytics":
            render_analytics_dashboard(services)
        elif item == "Reports":
            render_reports_dashboard(services)
            
    elif section == "Data Management":
        if item == "Hostages":
            render_hostages_management(services)
        elif item == "News Updates":
            render_news_management(services)
        elif item == "IDF Data":
            render_idf_data_management(services)
            
    elif section == "Analytics":
        if item == "Statistics":
            render_statistics(services)
        elif item == "Trends":
            render_trends(services)
        elif item == "Export":
            render_export_options(services)
            
    elif section == "Settings":
        if item == "Profile":
            render_profile_settings(services)
        elif item == "Preferences":
            render_preferences(services)
        elif item == "System":
            render_system_settings(services)

def render_analytics_dashboard(services: dict):
    st.title("Analytics Dashboard")
    data_service = services['data_service']
    chart_service = services['chart_service']
    
    # Load data
    hostages_data = data_service.load_hostages()
    if hostages_data.empty:
        st.warning("No data available for analysis")
        return
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    age_stats = data_service.get_age_statistics()
    
    with col1:
        st.metric("Average Age", f"{age_stats['average_age']:.1f}")
    with col2:
        st.metric("Youngest", age_stats['min_age'])
    with col3:
        st.metric("Oldest", age_stats['max_age'])
    
    # Charts
    tab1, tab2, tab3, tab4 = st.tabs([
        "Age Distribution", "Status Overview", 
        "Age Groups Analysis", "Timeline Analysis"
    ])
    
    with tab1:
        fig = chart_service.create_chart(hostages_data, "age_distribution")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = chart_service.create_chart(hostages_data, "status_pie")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = chart_service.create_chart(hostages_data, "age_group_bar")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        fig = chart_service.create_chart(hostages_data, "timeline_combined")
        if fig:
            st.plotly_chart(fig, use_container_width=True)

def render_reports_dashboard(services: dict):
    st.title("Reports Dashboard")
    st.info("Reports functionality coming soon...")

def render_hostages_management(services: dict):
    st.title("Hostages Management")
    data_service = services['data_service']
    hostages_data = data_service.load_hostages()
    if not hostages_data.empty:
        st.dataframe(hostages_data)

def render_news_management(services: dict):
    st.title("News Management")
    st.info("News management functionality coming soon...")

def render_idf_data_management(services: dict):
    st.title("IDF Data Management")
    data_service = services['data_service']
    hostages_data = data_service.load_hostages()
    if not hostages_data.empty:
        st.dataframe(hostages_data)
    else:
        st.warning("No data available")

def render_statistics(services: dict):
    st.title("Statistics")
    data_service = services['data_service']
    summary = data_service.get_hostages_summary()
    st.json(summary)

def render_trends(services: dict):
    st.title("Trends Analysis")
    st.info("Trends analysis coming soon...")

def render_export_options(services: dict):
    st.title("Export Options")
    st.info("Export functionality coming soon...")

def render_profile_settings(services: dict):
    st.title("Profile Settings")
    st.info("Profile settings coming soon...")

def render_preferences(services: dict):
    st.title("Preferences")
    st.info("Preferences coming soon...")

def render_system_settings(services: dict):
    st.title("System Settings")
    st.info("System settings coming soon...")

def render_hostages_gallery(services: dict):
    """Render hostages photo gallery"""
    st.title("Hostages Gallery")
    
    data_service = services['data_service']
    hostages_data = data_service.load_n12_hostages()
    
    if hostages_data.empty:
        st.warning("No hostage data available")
        return
    
    # Create grid of hostage cards
    cols = st.columns(4)
    for idx, hostage in hostages_data.iterrows():
        with cols[idx % 4]:
            if hostage['local_image_path'] and os.path.exists(hostage['local_image_path']):
                st.image(hostage['local_image_path'])
            st.markdown(f"""
                **{hostage['name']}**  
                Age: {hostage['age']}  
                Status: {hostage['status']}  
                Location: {hostage['location']}
            """)

def main():
    try:
        # Load configuration
        config = Config.load()
        
        # Page config
        st.set_page_config(
            page_title="Hostages Data Dashboard",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Initialize services
        services = initialize_services(config)
        
        # Render sidebar and get selection
        try:
            selected_section, selected_item = services['sidebar_menu'].render()
        except Exception as e:
            st.error(f"Error rendering sidebar: {str(e)}")
            selected_section, selected_item = None, None
        
        # Main content based on selection
        try:
            if selected_section and selected_item:
                render_selected_content(selected_section, selected_item, services)
            else:
                render_default_dashboard(services)
        except Exception as e:
            st.error(f"Error rendering content: {str(e)}")
            st.info("Please try refreshing the page or contact support if the issue persists.")
            
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please check your configuration and try again.")

if __name__ == "__main__":
    main()