import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import yaml

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="SocialPulse | סושיאל-פולס",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def setup_rtl_support():
    """Add RTL support for Hebrew"""
    rtl_css = """
        <style>
        .rtl {
            direction: rtl;
            text-align: right;
        }
        .stMarkdown, .stText {
            text-align: right;
        }
        .st-emotion-cache-1y4p8pa {
            direction: rtl;
        }
        .st-emotion-cache-16idsys p {
            text-align: right;
        }
        </style>
    """
    st.markdown(rtl_css, unsafe_allow_html=True)

def show_error(message):
    """Display error message"""
    st.error(f"🚫 {message}")

def show_success(message):
    """Display success message"""
    st.success(f"✅ {message}") 