import streamlit as st
from typing import Dict, Tuple
import os

class SidebarMenu:
    def __init__(self):
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
        image_path = "assets/images/profile.png"
        if os.path.exists(image_path):
            return image_path
        return "https://raw.githubusercontent.com/your-repo/assets/profile-placeholder.png"
    
    def render(self) -> Tuple[str, str]:
        # Add responsive styles
        st.sidebar.markdown("""
        <style>
        /* Desktop styles */
        .sidebar-menu-desktop {
            display: block;
        }
        .sidebar-menu-mobile {
            display: none;
        }
        
        /* Mobile styles */
        @media (max-width: 768px) {
            .sidebar-menu-desktop {
                display: none;
            }
            .sidebar-menu-mobile {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 1rem;
            }
            .mobile-icon {
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .mobile-icon:hover {
                background: rgba(255,255,255,0.2);
                transform: translateX(5px);
            }
            .mobile-menu-tooltip {
                position: absolute;
                left: 100%;
                background: rgba(0,0,0,0.8);
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                display: none;
            }
            .mobile-icon:hover .mobile-menu-tooltip {
                display: block;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        selected_section = None
        selected_item = None
        
        # Desktop Menu
        with st.sidebar:
            st.markdown('<div class="sidebar-menu-desktop">', unsafe_allow_html=True)
            
            # Profile Section
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(self.profile_image, width=60)
            with col2:
                st.markdown("### Admin User")
                st.markdown("System Administrator")
            
            st.markdown("---")
            
            # Full Menu
            for section, details in self.menu_items.items():
                with st.expander(f"{details['icon']} {section}", expanded=True):
                    for item in details['items']:
                        if st.button(
                            item,
                            key=f"desktop-{section}-{item}",
                            help=f"Navigate to {section} - {item}",
                            use_container_width=True
                        ):
                            selected_section = section
                            selected_item = item
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Mobile Menu (Icons only)
            st.markdown('<div class="sidebar-menu-mobile">', unsafe_allow_html=True)
            
            # Mobile Profile Icon
            st.markdown(f"""
                <div class="mobile-icon">
                    👤
                    <span class="mobile-menu-tooltip">Admin User</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Mobile Menu Icons
            for section, details in self.menu_items.items():
                if st.button(
                    details['icon'],
                    key=f"mobile-{section}",
                    help=section,
                    use_container_width=False
                ):
                    selected_section = section
                    selected_item = details['items'][0]  # Default to first item
                    
            st.markdown('</div>', unsafe_allow_html=True)
        
        return selected_section, selected_item