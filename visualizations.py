import plotly.express as px
import plotly.graph_objects as go

def create_time_series(data, value_col='value', date_col='date'):
    """Create time series plot"""
    fig = px.line(data, x=date_col, y=value_col, 
                  title='Time Series Analysis')
    return fig

def create_category_distribution(data, category_col='category'):
    """Create category distribution plot"""
    category_counts = data[category_col].value_counts()
    fig = px.bar(x=category_counts.index, y=category_counts.values,
                 title='Category Distribution')
    return fig

def create_scatter_plot(data, x_col, y_col, color_col=None):
    """Create scatter plot"""
    fig = px.scatter(data, x=x_col, y=y_col, color=color_col,
                    title=f'{x_col} vs {y_col}')
    return fig

def create_metrics_cards(stats):
    """Create metrics display"""
    return {
        'Mean': stats['value']['mean'],
        'Median': stats['value']['50%'],
        'Std Dev': stats['value']['std'],
        'Count': stats['value']['count']
    } 