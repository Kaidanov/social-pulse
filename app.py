import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from src.data.data_processor import DataProcessor
from src.visualization.plots import (create_time_series, create_category_distribution,
                                   create_age_distribution, create_social_metrics)
from src.utils.helpers import set_page_config, setup_rtl_support, show_error, show_success, get_translation
from src.data.data_loader import IsraeliCrisisDataLoader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize data loader with config
config = {
    'twitter_api_key': os.getenv('TWITTER_BEARER_TOKEN'),
    'cache_dir': '.cache',
    'data_dir': 'data'
}

def display_data_overview(df, lang='he'):
    """Display overview metrics for the loaded data"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(get_translation('total_records', lang), f"{len(df):,}")
    
    # Handle social media data
    if 'text' in df.columns and 'date' in df.columns:
        with col2:
            st.metric(
                get_translation('date_range', lang),
                f"{pd.to_datetime(df['date'].min()).strftime('%d/%m/%y')} - {pd.to_datetime(df['date'].max()).strftime('%d/%m/%y')}"
            )
        with col3:
            st.metric(get_translation('total_likes', lang), f"{df['likes'].sum():,}")
        with col4:
            st.metric(get_translation('total_shares', lang), f"{df['retweets'].sum():,}")
    
    # Handle hostage data
    elif any(col in df.columns for col in ['תאריך_חטיפה', 'kidnap_date', 'date_of_kidnapping']):
        date_col = next(col for col in ['תאריך_חטיפה', 'kidnap_date', 'date_of_kidnapping'] if col in df.columns)
        with col2:
            st.metric(
                get_translation('date_range', lang),
                f"{pd.to_datetime(df[date_col].min()).strftime('%d/%m/%y')} - {pd.to_datetime(df[date_col].max()).strftime('%d/%m/%y')}"
            )
        
        status_col = next(col for col in ['סטטוס', 'status'] if col in df.columns)
        status_counts = df[status_col].value_counts()
        
        with col3:
            st.metric(get_translation('in_captivity', lang), 
                     f"{status_counts.get('בשבי', status_counts.get('In Captivity', 0)):,}")
        with col4:
            st.metric(get_translation('released', lang), 
                     f"{status_counts.get('שוחרר', status_counts.get('Released', 0)):,}")

def display_insights(df, lang='he'):
    """Display key insights from the data"""
    if 'text' in df.columns:  # Social media data
        # Calculate social media insights
        total_posts = len(df)
        total_likes = df['likes'].sum()
        total_retweets = df['retweets'].sum()
        avg_engagement = (total_likes + total_retweets) / total_posts if total_posts > 0 else 0
        
        # Display social media insights in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **{get_translation('social_media_summary', lang)}**
            - {get_translation('total_posts', lang)}: {total_posts:,}
            - {get_translation('total_engagement', lang)}: {total_likes + total_retweets:,}
            - {get_translation('avg_engagement', lang)}: {avg_engagement:.1f}
            """)
        
        with col2:
            st.warning(f"""
            **{get_translation('engagement_breakdown', lang)}**
            - {get_translation('total_likes', lang)}: {total_likes:,}
            - {get_translation('total_retweets', lang)}: {total_retweets:,}
            - {get_translation('engagement_rate', lang)}: {(avg_engagement/total_posts*100):.1f}%
            """)
        
        with col3:
            # Calculate posts per day
            df['date'] = pd.to_datetime(df['date'])
            posts_by_day = df.groupby(df['date'].dt.date).size()
            st.error(f"""
            **{get_translation('posting_patterns', lang)}**
            - {get_translation('days_analyzed', lang)}: {len(posts_by_day)}
            - {get_translation('posts_per_day', lang)}: {posts_by_day.mean():.1f}
            - {get_translation('peak_day', lang)}: {posts_by_day.idxmax().strftime('%d/%m/%y')}
            """)
            
    else:  # Hostage data
        # Calculate hostage insights
        total_hostages = len(df)
        in_captivity = len(df[df['סטטוס'] == 'בשבי']) if 'סטטוס' in df.columns else 0
        released = len(df[df['סטטוס'] == 'שוחרר']) if 'סטטוס' in df.columns else 0
        killed = len(df[df['סטטוס'] == 'נרצח']) if 'סטטוס' in df.columns else 0
        unknown = len(df[df['סטטוס'] == 'מצב לא ידוע']) if 'סטטוס' in df.columns else 0
        children = len(df[df['קבוצת_גיל'] == 'ילד']) if 'קבוצת_גיל' in df.columns else 0
        elderly = len(df[df['קבוצת_גיל'] == 'קשיש']) if 'קבוצת_גיל' in df.columns else 0
        days_in_captivity = (datetime.now() - pd.to_datetime('2023-10-07')).days
        
        # Display hostage insights in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **{get_translation('hostages_summary', lang)}**
            - {get_translation('total_hostages', lang)}: {total_hostages}
            - {get_translation('in_captivity', lang)}: {in_captivity}
            - {get_translation('released', lang)}: {released}
            - {get_translation('killed', lang)}: {killed}
            - {get_translation('unknown', lang)}: {unknown}
            """)
        
        with col2:
            st.warning(f"""
            **{get_translation('vulnerable_groups', lang)}**
            - {get_translation('children', lang)}: {children}
            - {get_translation('elderly', lang)}: {elderly}
            - {get_translation('days_in_captivity', lang)}: {days_in_captivity}
            """)
        
        with col3:
            if 'עיר' in df.columns:
                cities_affected = df['עיר'].value_counts()
                st.error(f"""
                **{get_translation('cities_affected', lang)}**
                {cities_affected.head(5).to_string()}
                """)
            else:
                st.error(f"""
                **{get_translation('data_summary', lang)}**
                {get_translation('no_city_data', lang)}
                """)

def add_search_configuration():
    """Add search configuration options"""
    with st.sidebar.expander(get_translation('search_config', st.session_state.language)):
        # Date range selector
        start_date = st.date_input(
            get_translation('start_date', st.session_state.language),
            value=datetime(2023, 10, 7)
        )
        end_date = st.date_input(
            get_translation('end_date', st.session_state.language),
            value=datetime.now()
        )
        
        # Status filter
        status_options = ['All', 'בשבי/In Captivity', 'שוחרר/Released']
        selected_status = st.selectbox(
            get_translation('status_filter', st.session_state.language),
            status_options
        )
        
        # Age group filter
        age_options = ['All', 'ילד/Child', 'מבוגר/Adult', 'קשיש/Elderly']
        selected_age = st.selectbox(
            get_translation('age_filter', st.session_state.language),
            age_options
        )
        
        # Search terms
        search_terms = st.text_input(
            get_translation('search_terms', st.session_state.language),
            placeholder="Enter search terms..."
        )
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'status': selected_status,
            'age_group': selected_age,
            'search_terms': search_terms
        }

def filter_data(df, config):
    """Filter data based on configuration"""
    if df is None:
        return pd.DataFrame()
        
    filtered_df = df.copy()
    
    # Date filter
    if 'תאריך_חטיפה' in filtered_df.columns:
        try:
            # Convert date column to datetime if it's not already
            filtered_df['תאריך_חטיפה'] = pd.to_datetime(filtered_df['תאריך_חטיפה'])
            # Convert config dates to pandas datetime
            start_date = pd.to_datetime(config['start_date'])
            end_date = pd.to_datetime(config['end_date'])
            
            # Apply date filter
            filtered_df = filtered_df[
                (filtered_df['תאריך_חטיפה'] >= start_date) &
                (filtered_df['תאריך_חטיפה'] <= end_date)
            ]
        except Exception as e:
            st.error(f"Error filtering dates: {str(e)}")
            return filtered_df
    
    # Handle social media data
    elif 'date' in filtered_df.columns:
        try:
            filtered_df['date'] = pd.to_datetime(filtered_df['date'])
            start_date = pd.to_datetime(config['start_date'])
            end_date = pd.to_datetime(config['end_date'])
            
            filtered_df = filtered_df[
                (filtered_df['date'] >= start_date) &
                (filtered_df['date'] <= end_date)
            ]
        except Exception as e:
            st.error(f"Error filtering social media dates: {str(e)}")
            return filtered_df
    
    # Status filter
    if config['status'] != 'All' and 'סטטוס' in filtered_df.columns:
        status = config['status'].split('/')[0]  # Get Hebrew status
        filtered_df = filtered_df[filtered_df['סטטוס'] == status]
    
    # Age group filter
    if config['age_group'] != 'All' and 'קבוצת_גיל' in filtered_df.columns:
        age_group = config['age_group'].split('/')[0]  # Get Hebrew age group
        filtered_df = filtered_df[filtered_df['קבוצת_גיל'] == age_group]
    
    # Search terms
    if config['search_terms']:
        try:
            terms = config['search_terms'].lower().split()
            # Search in text column for social media data
            if 'text' in filtered_df.columns:
                mask = filtered_df['text'].str.lower().apply(lambda x: any(term in str(x) for term in terms))
            # Search in name column for hostage data
            elif 'שם' in filtered_df.columns:
                mask = filtered_df['שם'].str.lower().apply(lambda x: any(term in str(x) for term in terms))
            else:
                mask = pd.Series([True] * len(filtered_df))
            filtered_df = filtered_df[mask]
        except Exception as e:
            st.error(f"Error applying search terms: {str(e)}")
    
    return filtered_df

def create_status_pie_chart(df):
    """Create pie chart for hostage status distribution"""
    try:
        if 'סטטוס' not in df.columns:
            st.error("No status data available")
            return None
            
        status_counts = df['סטטוס'].value_counts()
        if status_counts.empty:
            st.error("No status data available")
            return None
            
        fig = px.pie(values=status_counts.values, 
                     names=status_counts.index,
                     title='התפלגות סטטוס חטופים')
        fig.update_layout(
            title_x=0.5,
            title_font=dict(size=20),
            font=dict(size=14)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating status chart: {str(e)}")
        return None

def create_age_group_bar(df):
    """Create bar chart for age group distribution"""
    try:
        if 'קבוצת_גיל' not in df.columns:
            st.warning("No age group data available")
            return None
            
        age_counts = df['קבוצת_גיל'].value_counts()
        fig = px.bar(x=age_counts.index, 
                     y=age_counts.values,
                     title='התפלגות קבוצות גיל',
                     labels={'x': 'קבוצת גיל', 'y': 'מספר חטופים'})
        fig.update_layout(
            title_x=0.5,
            title_font=dict(size=20),
            font=dict(size=14)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating age group chart: {str(e)}")
        return None

def create_timeline_chart(df):
    """Create timeline visualization based on data type"""
    try:
        if 'text' in df.columns:  # Social media data
            daily_engagement = df.groupby('date').agg({
                'likes': 'sum',
                'retweets': 'sum'
            }).reset_index()
            
            fig = px.line(daily_engagement, x='date', 
                         y=['likes', 'retweets'],
                         title='מדדי אינטראקציה לאורך זמן',
                         labels={'value': 'כמות', 'date': 'תאריך', 
                                'variable': 'סוג'})
        else:  # Hostage data
            if 'תאריך_חטיפה' not in df.columns:
                st.warning("No date data available")
                return None
                
            daily_counts = df.groupby(['תאריך_חטי��ה', 'סטטוס']).size().unstack(fill_value=0)
            fig = px.line(daily_counts, 
                         title='מספר חטופים לורך זמן לפי סטטוס',
                         labels={'value': 'מספר חטופים', 'תאריך_חטיפה': 'תאריך'})
        
        fig.update_layout(
            title_x=0.5,
            title_font=dict(size=20),
            font=dict(size=14)
        )
        return fig
    except Exception as e:
        st.error(f"Error creating timeline chart: {str(e)}")
        return None

def display_data_source_info(source_type: str, lang: str, df: pd.DataFrame = None):
    """Display detailed information about the data source"""
    sources = {
        'initial_data': {
            'name': {'he': 'מאגר נתונים מאומת', 'en': 'Verified Database'},
            'organization': {'he': 'פורום משפחות החטופים והנעדרים', 'en': 'Hostages and Missing Families Forum'},
            'link': 'https://www.bring-them-home-now.com/',
            'description': {
                'he': 'נתונים מאומתים ע״י פורום המשפחות ומשרד החוץ',
                'en': 'Data verified by the Families Forum and Ministry of Foreign Affairs'
            },
            'last_update': '2024-01-14',
            'update_frequency': {'he': 'מתעדכן יומית', 'en': 'Updated daily'}
        },
        'official_data': {
            'name': {'he': 'נתוני משרד החוץ', 'en': 'MFA Data'},
            'organization': {'he': 'משרד החוץ הישראלי', 'en': 'Israeli Ministry of Foreign Affairs'},
            'link': 'https://www.gov.il/he/departments/general/kidnapped_and_missing_oct_2023',
            'description': {
                'he': 'נתונים רשמיים מטעם מדינת ישראל',
                'en': 'Official data from the State of Israel'
            },
            'last_update': '2024-01-14',
            'update_frequency': {'he': 'מתעדכן מספר פעמים ביום', 'en': 'Updated several times daily'}
        },
        'idf_data': {
            'name': {'he': 'נתוני צה"ל', 'en': 'IDF Data'},
            'organization': {'he': 'דובר צה"ל', 'en': 'IDF Spokesperson'},
            'link': 'https://www.idf.il/en/minisites/hostages/',
            'description': {
                'he': 'נתונים מאומתים ע״י צה"ל',
                'en': 'Data verified by the IDF'
            },
            'last_update': '2024-01-14',
            'update_frequency': {'he': 'מתעדכן יומית', 'en': 'Updated daily'}
        },
        'social_media': {
            'name': {'he': 'רשתות חברתיות', 'en': 'Social Media'},
            'organization': {'he': 'X/Twitter', 'en': 'X/Twitter'},
            'link': 'https://twitter.com/search?q=%23BringThemHomeNow',
            'description': {
                'he': 'נתונים מרשתות חברתיות בזמן אמת',
                'en': 'Real-time data from social media platforms'
            },
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'update_frequency': {'he': 'מתעדכן בזמן אמת', 'en': 'Real-time updates'}
        }
    }
    
    if source_type in sources:
        source = sources[source_type]
        st.sidebar.markdown("---")
        
        # Source header with organization logo/icon
        st.sidebar.markdown(f"""
        ### {get_translation('data_source_info', lang)}
        #### {source['name'][lang]}
        **{source['organization'][lang]}**
        """)
        
        # Dataset statistics
        if df is not None:
            st.sidebar.markdown(f"""
            **{get_translation('dataset_stats', lang)}:**
            - {get_translation('total_records', lang)}: {len(df):,}
            - {get_translation('date_range', lang)}: {df['תאריך_חטיפה'].min().strftime('%d/%m/%y')} - {df['תאריך_חטיפה'].max().strftime('%d/%m/%y')}
            """)
        
        # Update information
        st.sidebar.markdown(f"""
        **{get_translation('update_info', lang)}:**
        - {get_translation('last_update', lang)}: {source['last_update']}
        - {source['update_frequency'][lang]}
        """)
        
        # Source description
        st.sidebar.markdown(f"_{source['description'][lang]}_")
        
        # Source link
        st.sidebar.markdown(f"[{get_translation('view_source', lang)}]({source['link']})")
        
        st.sidebar.markdown("---")

def main():
    # Initialize page config
    set_page_config()
    
    # Initialize session state variables
    if 'language' not in st.session_state:
        st.session_state.language = 'he'
    
    if 'data_loader' not in st.session_state:
        st.session_state.data_loader = IsraeliCrisisDataLoader(config)
    
    if 'initial_data' not in st.session_state:
        st.session_state.initial_data = st.session_state.data_loader.load_initial_hostages_data()
    
    if 'current_data' not in st.session_state:
        st.session_state.current_data = st.session_state.initial_data.copy() if st.session_state.initial_data is not None else pd.DataFrame()
    
    # Add language selector to the top of the sidebar
    lang_col1, lang_col2 = st.sidebar.columns(2)
    with lang_col1:
        if st.button('🇮🇱 עברית'):
            st.session_state.language = 'he'
            st.rerun()
    with lang_col2:
        if st.button('🇺🇸 English'):
            st.session_state.language = 'en'
            st.rerun()
    
    # Setup RTL/LTR based on language
    setup_rtl_support(is_hebrew=(st.session_state.language == 'he'))
    
    # Rest of your code, using translations
    st.sidebar.title(get_translation('controls', st.session_state.language))
    
    # Data source selector with translations
    data_source = st.sidebar.selectbox(
        get_translation('select_data_source', st.session_state.language),
        [
            get_translation('initial_data', st.session_state.language),
            get_translation('sample_data', st.session_state.language),
            get_translation('official_data', st.session_state.language),
            get_translation('social_media', st.session_state.language)
        ]
    )

    # Handle data loading based on source
    if data_source == get_translation('initial_data', st.session_state.language):
        st.session_state.current_data = st.session_state.initial_data.copy()
        show_success(
            "Initial data loaded!" if st.session_state.language == 'en' else "נתונים ראשוניים נטענו!",
            st.session_state.language
        )
        display_data_source_info('initial_data', st.session_state.language, st.session_state.current_data)
    
    elif data_source == get_translation('sample_data', st.session_state.language):
        if st.sidebar.button(get_translation('generate_sample', st.session_state.language)):
            st.session_state.current_data = st.session_state.data_loader.generate_sample_hostages_data()
            show_success(
                "Sample data generated successfully!" if st.session_state.language == 'en' else "נתוני דוגמה נוצרו בהצלחה!",
                st.session_state.language
            )
    
    elif data_source == get_translation('official_data', st.session_state.language):
        if st.sidebar.button(get_translation('load_official', st.session_state.language)):
            st.session_state.current_data = st.session_state.data_loader.load_hostages_data_from_gov()
            show_success(
                "Official data loaded successfully!" if st.session_state.language == 'en' else "הנתונים נטענו בהצלחה!",
                st.session_state.language
            )
            display_data_source_info('official_data', st.session_state.language, st.session_state.current_data)
    
    elif data_source == get_translation('social_media', st.session_state.language):
        query = st.sidebar.text_input(get_translation('search', st.session_state.language), value="#BringThemHomeNow")
        if st.sidebar.button(get_translation('load_social', st.session_state.language)):
            st.session_state.current_data = st.session_state.data_loader.fetch_x_data(query=query)
            show_success(
                "Social media data loaded successfully!" if st.session_state.language == 'en' else "נתוני רשתות חברתיות נטענו בהצלחה!",
                st.session_state.language
            )
            display_data_source_info('social_media', st.session_state.language)

    # Add search configuration
    search_config = add_search_configuration()
    
    # Handle data loading and filtering
    if st.session_state.current_data is not None and not st.session_state.current_data.empty:
        df = st.session_state.current_data
        
        # Filter data based on configuration
        filtered_df = filter_data(df, search_config)
        
        if filtered_df.empty:
            st.warning(get_translation('no_matching_data', st.session_state.language))
        else:
            # Display data overview
            st.header(get_translation('data_overview', st.session_state.language))
            display_data_overview(filtered_df, st.session_state.language)
            
            # Display insights
            display_insights(filtered_df, st.session_state.language)
            
            # Create visualization tabs
            if 'text' in filtered_df.columns:  # Social media data
                tab1, tab2 = st.tabs([
                    get_translation('engagement_metrics', st.session_state.language),
                    get_translation('data_analysis', st.session_state.language)
                ])
                
                with tab1:
                    time_fig = create_time_series(filtered_df)
                    if time_fig:
                        st.plotly_chart(time_fig, use_container_width=True)
                    
                    metrics_fig = create_social_metrics(filtered_df)
                    if metrics_fig:
                        st.plotly_chart(metrics_fig, use_container_width=True)
                
                with tab2:
                    # Add analysis tools and data table
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader(get_translation('trending_hashtags', st.session_state.language))
                        hashtags = filtered_df['text'].str.findall(r'#\w+').explode().value_counts().head(10)
                        st.bar_chart(hashtags)
                        
                    with col2:
                        st.subheader(get_translation('engagement_patterns', st.session_state.language))
                        hourly_engagement = filtered_df.groupby(pd.to_datetime(filtered_df['date']).dt.hour)['likes'].mean()
                        st.line_chart(hourly_engagement)
                    
                    # Data table with search
                    st.subheader(get_translation('search_data', st.session_state.language))
                    search_term = st.text_input(
                        get_translation('search_posts', st.session_state.language),
                        key='social_search'
                    )
                    
                    display_df = filtered_df
                    if search_term:
                        mask = filtered_df['text'].str.contains(search_term, case=False, na=False)
                        display_df = filtered_df[mask]
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        column_config={
                            'date': st.column_config.DatetimeColumn('Date & Time'),
                            'text': st.column_config.TextColumn('Content'),
                            'likes': st.column_config.NumberColumn('Likes'),
                            'retweets': st.column_config.NumberColumn('Retweets')
                        }
                    )

            else:  # Hostage data
                tab1, tab2, tab3 = st.tabs([
                    get_translation('status_and_demographics', st.session_state.language),
                    get_translation('timeline_analysis', st.session_state.language),
                    get_translation('detailed_data', st.session_state.language)
                ])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        status_fig = create_category_distribution(filtered_df)
                        if status_fig:
                            st.plotly_chart(status_fig, use_container_width=True)
                    
                    with col2:
                        age_fig = create_age_distribution(filtered_df)
                        if age_fig:
                            st.plotly_chart(age_fig, use_container_width=True)
                
                with tab2:
                    time_fig = create_time_series(filtered_df)
                    if time_fig:
                        st.plotly_chart(time_fig, use_container_width=True)
                    
                    # Add timeline analysis
                    st.subheader(get_translation('key_events', st.session_state.language))
                    events_df = filtered_df[filtered_df['סטטוס'].isin(['שוחרר', 'נרצח'])].sort_values('תאריך_עדכון')
                    st.dataframe(
                        events_df[['תאריך_עדכון', 'שם', 'סטטוס', 'עיר']],
                        use_container_width=True,
                        hide_index=True
                    )
                
                with tab3:
                    # Data analysis tools and table
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader(get_translation('filter_data', st.session_state.language))
                        selected_status = st.multiselect(
                            get_translation('status_filter', st.session_state.language),
                            filtered_df['סטטוס'].unique()
                        )
                        
                        selected_cities = st.multiselect(
                            get_translation('city_filter', st.session_state.language),
                            filtered_df['עיר'].unique()
                        )
                    
                    with col2:
                        st.subheader(get_translation('search_data', st.session_state.language))
                        name_search = st.text_input(
                            get_translation('search_names', st.session_state.language)
                        )
                    
                    # Apply filters
                    display_df = filtered_df.copy()
                    if selected_status:
                        display_df = display_df[display_df['סטטוס'].isin(selected_status)]
                    if selected_cities:
                        display_df = display_df[display_df['עיר'].isin(selected_cities)]
                    if name_search:
                        display_df = display_df[display_df['שם'].str.contains(name_search, case=False, na=False)]
                    
                    # Display filtered data
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        column_config={
                            'שם': st.column_config.TextColumn('Name/שם'),
                            'גיל': st.column_config.NumberColumn('Age/גיל'),
                            'עיר': st.column_config.TextColumn('City/עיר'),
                            'סטטוס': st.column_config.TextColumn('Status/סטטוס'),
                            'תאריך_חטיפה': st.column_config.DateColumn('Kidnap Date/תאריך חטיפה'),
                            'ימים_בשבי': st.column_config.NumberColumn('Days/ימים'),
                            'קבוצת_גיל': st.column_config.TextColumn('Age Group/קבוצת גיל')
                        }
                    )
    else:
        st.info(get_translation('no_data', st.session_state.language))

if __name__ == "__main__":
    main()