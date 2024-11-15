import logging
import streamlit as st
from datetime import datetime
import os

class Logger:
    def __init__(self, name: str, log_dir: str = "logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        os.makedirs(log_dir, exist_ok=True)
        
        # File handler
        fh = logging.FileHandler(
            os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")
        )
        fh.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        
        self.logger.addHandler(fh)
    
    def info(self, message: str):
        self.logger.info(message)
        st.info(message)
    
    def error(self, message: str):
        self.logger.error(message)
        st.error(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
        st.warning(message)
    
    def success(self, message: str):
        self.logger.info(f"SUCCESS: {message}")
        st.success(message) 