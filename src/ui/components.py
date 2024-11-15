import streamlit as st
from typing import Dict, Tuple
import os

class SidebarMenu:
    def __init__(self):
        if 'current_section' not in st.session_state:
            st.session_state.current_section = None
        if 'current_item' not in st.session_state:
            st.session_state.current_item = None
            
        self.menu_items = {
            "Dashboard": {
                "icon": "📊",
                "items": ["Overview", "Analytics", "Reports"]
            },
            "Data Management": {
                "icon": "📁",
                "items": ["Hostages", "News Updates", "IDF Data"]
            },
            "Analytics": {
                "icon": "📈",
                "items": ["Statistics", "Trends", "Export"]
            },
            "Settings": {
                "icon": "⚙️",
                "items": ["Profile", "Preferences", "System"]
            }
        }
        
        self.profile_image = self.get_profile_image()
    
    def get_profile_image(self) -> str:
        """Get profile image with fallback"""
        image_paths = [
            "assets/images/profile.png",
            "src/assets/images/profile.png",
            "profile.png"
        ]
        
        for path in image_paths:
            if os.path.exists(path):
                return path
                
        return "https://raw.githubusercontent.com/streamlit/streamlit/develop/examples/data/avatar.jpg"
    
    def handle_menu_click(self, section: str, item: str):
        """Handle menu item click"""
        st.session_state.current_section = section
        st.session_state.current_item = item
    
    def render(self) -> Tuple[str, str]:
        with st.sidebar:
            # Profile Section
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(self.profile_image, width=60)
            with col2:
                st.markdown("### Admin User")
                st.markdown("System Administrator")
            
            st.markdown("---")
            
            # Menu with single expander
            for section, details in self.menu_items.items():
                # Use markdown for section header
                st.markdown(f"### {details['icon']} {section}")
                
                # Create buttons for items
                for item in details['items']:
                    is_active = (st.session_state.current_section == section and 
                               st.session_state.current_item == item)
                    
                    if st.button(
                        item,
                        key=f"{section}-{item}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary"
                    ):
                        self.handle_menu_click(section, item)
                
                st.markdown("---")
            
            return st.session_state.current_section, st.session_state.current_item