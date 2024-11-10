import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict

def create_time_series(data: pd.DataFrame, value_col='value', date_col='date') -> go.Figure:
    """Create time series plot"""
    fig = px.line(data, x=date_col, y=value_col, 
                  title='Time Series Analysis')
    return fig

def create_category_distribution(data: pd.DataFrame, category_col='category') -> go.Figure:
    """Create category distribution plot"""
    category_counts = data[category_col].value_counts()
    fig = px.bar(x=category_counts.index, y=category_counts.values,
                 title='Category Distribution')
    return fig

def create_scatter_plot(data: pd.DataFrame, x_col: str, y_col: str, 
                       color_col: str = None) -> go.Figure:
    """Create scatter plot"""
    fig = px.scatter(data, x=x_col, y=y_col, color=color_col,
                    title=f'{x_col} vs {y_col}')
    return fig 