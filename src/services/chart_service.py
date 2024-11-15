from src.core.interfaces import IChartService
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional

class ChartService(IChartService):
    def __init__(self):
        self.color_scheme = {
            'primary': '#1f77b4',
            'success': '#51cf66',
            'danger': '#ff6b6b',
            'warning': '#ffd43b',
            'info': '#4dabf7'
        }
        
        self.chart_config = {
            'age_distribution': {
                'title': 'Age Distribution of Hostages',
                'xaxis_title': 'Age',
                'yaxis_title': 'Number of People'
            },
            'status_timeline': {
                'title': 'Status Changes Over Time',
                'xaxis_title': 'Date',
                'yaxis_title': 'Number of People'
            },
            'location_map': {
                'title': 'Hostage Locations',
                'zoom': 7
            }
        }

    def create_chart(self, data: pd.DataFrame, chart_type: str) -> Optional[go.Figure]:
        chart_methods = {
            'age_distribution': self._create_age_distribution,
            'status_timeline': self._create_status_timeline,
            'location_map': self._create_location_map,
            'status_pie': self._create_status_pie,
            'age_group_bar': self._create_age_group_bar,
            'timeline_combined': self._create_timeline_combined
        }
        
        method = chart_methods.get(chart_type)
        return method(data) if method else None

    def _create_age_distribution(self, df: pd.DataFrame) -> go.Figure:
        if 'age' not in df.columns:
            return None
            
        fig = px.histogram(
            df,
            x='age',
            nbins=20,
            color_discrete_sequence=[self.color_scheme['primary']],
            title=self.chart_config['age_distribution']['title']
        )
        
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=40, l=0, r=0, b=0),
            xaxis_title=self.chart_config['age_distribution']['xaxis_title'],
            yaxis_title=self.chart_config['age_distribution']['yaxis_title']
        )
        
        # Add age group annotations
        age_groups = df['age'].value_counts(bins=5).sort_index()
        for i, (age_range, count) in enumerate(age_groups.items()):
            fig.add_annotation(
                x=age_range.mid,
                y=count,
                text=f"{count} people",
                showarrow=True,
                arrowhead=1
            )
        
        return fig

    def _create_status_pie(self, df: pd.DataFrame) -> go.Figure:
        if 'status' not in df.columns:
            return None
            
        status_counts = df['status'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=.3,
            marker_colors=[self.color_scheme[status.lower()] for status in status_counts.index]
        )])
        
        fig.update_layout(
            title='Hostage Status Distribution',
            annotations=[dict(text='Status', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig

    def _create_age_group_bar(self, df: pd.DataFrame) -> go.Figure:
        if 'age' not in df.columns or 'status' not in df.columns:
            return None
            
        df['age_group'] = pd.cut(df['age'], bins=[0, 18, 30, 50, 70, 100], 
                                labels=['0-18', '19-30', '31-50', '51-70', '70+'])
        
        fig = px.bar(
            df.groupby(['age_group', 'status']).size().unstack(),
            barmode='group',
            color_discrete_map={
                'Released': self.color_scheme['success'],
                'Held': self.color_scheme['danger'],
                'Deceased': self.color_scheme['warning']
            }
        )
        
        fig.update_layout(
            title='Age Groups by Status',
            xaxis_title='Age Group',
            yaxis_title='Number of People',
            legend_title='Status'
        )
        
        return fig

    def _create_timeline_combined(self, df: pd.DataFrame) -> go.Figure:
        if 'date' not in df.columns or 'status' not in df.columns:
            return None
            
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=('Daily Status Changes', 'Cumulative Changes'))
        
        # Daily changes
        daily_status = df.groupby(['date', 'status']).size().unstack().fillna(0)
        
        for status in daily_status.columns:
            fig.add_trace(
                go.Scatter(x=daily_status.index, y=daily_status[status], 
                          name=f'Daily {status}', mode='lines+markers'),
                row=1, col=1
            )
        
        # Cumulative changes
        cumulative_status = daily_status.cumsum()
        
        for status in cumulative_status.columns:
            fig.add_trace(
                go.Scatter(x=cumulative_status.index, y=cumulative_status[status], 
                          name=f'Total {status}', mode='lines'),
                row=2, col=1
            )
        
        fig.update_layout(height=800, showlegend=True)
        
        return fig

    def _create_status_timeline(self, df: pd.DataFrame) -> go.Figure:
        if 'status' not in df.columns or 'date' not in df.columns:
            return None
            
        status_counts = df.groupby(['date', 'status']).size().reset_index(name='count')
        fig = px.line(
            status_counts,
            x='date',
            y='count',
            color='status',
            title='Status Changes Over Time'
        )
        return fig

    def _create_location_map(self, df: pd.DataFrame) -> go.Figure:
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            return None
            
        fig = px.scatter_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            hover_name='name' if 'name' in df.columns else None,
            zoom=7,
            title='Hostage Locations'
        )
        fig.update_layout(mapbox_style='carto-positron')
        return fig