import streamlit as st

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Data Analysis App",
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
        </style>
    """
    st.markdown(rtl_css, unsafe_allow_html=True)

def show_error(message):
    """Display error message"""
    st.error(message)

def show_success(message):
    """Display success message"""
    st.success(message) 