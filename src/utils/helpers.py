import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="SocialPulse | סושיאל-פולס",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def setup_rtl_support(is_hebrew=True):
    """Add RTL/LTR support based on language"""
    if is_hebrew:
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
    else:
        rtl_css = """
            <style>
            .rtl {
                direction: ltr;
                text-align: left;
            }
            .stMarkdown, .stText {
                text-align: left;
            }
            .st-emotion-cache-1y4p8pa {
                direction: ltr;
            }
            .st-emotion-cache-16idsys p {
                text-align: left;
            }
            </style>
        """
    st.markdown(rtl_css, unsafe_allow_html=True)

def show_error(message, lang='he'):
    """Display error message in Hebrew/English"""
    prefix = "🚫" if lang == 'he' else "Error:"
    st.error(f"{prefix} {message}")

def show_success(message, lang='he'):
    """Display success message in Hebrew/English"""
    prefix = "✅" if lang == 'he' else "Success:"
    st.success(f"{prefix} {message}")

def show_info(message, lang='he'):
    """Display info message in Hebrew/English"""
    prefix = "ℹ️" if lang == 'he' else "Info:"
    st.info(f"{prefix} {message}")

# Add translations dictionary
TRANSLATIONS = {
    'controls': {'he': 'בקרים', 'en': 'Controls'},
    'select_data_source': {'he': 'בחר מקור נתונים', 'en': 'Select Data Source'},
    'sample_data': {'he': 'נתוני דוגמה', 'en': 'Sample Data'},
    'official_data': {'he': 'נתונים רשמיים', 'en': 'Official Data'},
    'social_media': {'he': 'רשתות חברתיות', 'en': 'Social Media'},
    'generate_sample': {'he': 'יצירת נתונ דוגמה', 'en': 'Generate Sample Data'},
    'load_official': {'he': 'טעינת נתונים רשמיים', 'en': 'Load Official Data'},
    'load_social': {'he': 'טעינת נתוני רשתות חברתיות', 'en': 'Load Social Media Data'},
    'search': {'he': 'חיפוש', 'en': 'Search'},
    'data_overview': {'he': 'סקירת נתונים', 'en': 'Data Overview'},
    'total_records': {'he': 'סך הכל רשומות', 'en': 'Total Records'},
    'date_range': {'he': 'טווח תאריכים', 'en': 'Date Range'},
    'in_captivity': {'he': 'בשבי', 'en': 'In Captivity'},
    'released': {'he': 'שוחררו', 'en': 'Released'},
    'total_likes': {'he': 'סה״כ לייקים', 'en': 'Total Likes'},
    'total_shares': {'he': 'סה״כ שיתופים', 'en': 'Total Shares'},
    'engagement_metrics': {'he': 'מדדי אינטראקציה', 'en': 'Engagement Metrics'},
    'raw_data': {'he': 'נתונים גולמיים', 'en': 'Raw Data'},
    'status_distribution': {'he': 'התפלגות סטטוס', 'en': 'Status Distribution'},
    'age_distribution': {'he': 'התפלגות גיל', 'en': 'Age Distribution'},
    'timeline': {'he': 'נתונים לאורך זמן', 'en': 'Timeline'},
    'select_language': {'he': 'בחר שפה', 'en': 'Select Language'},
    'hebrew': {'he': 'עברית', 'en': 'Hebrew'},
    'english': {'he': 'אנגלית', 'en': 'English'},
    'initial_data': {'he': 'נתונים ראשוניים', 'en': 'Initial Data'},
    'no_data': {'he': 'אין נתונים זמינים', 'en': 'No data available'},
    'data_loaded': {'he': 'הנתונים נטענו בהצלחה', 'en': 'Data loaded successfully'},
    'hostages_overview': {'he': 'סקירת חטופים', 'en': 'Hostages Overview'},
    'total_hostages': {'he': 'סה״כ חטופים', 'en': 'Total Hostages'},
    'in_captivity_count': {'he': 'בשבי', 'en': 'In Captivity'},
    'released_count': {'he': 'שוחררו', 'en': 'Released'},
    'days_since_oct7': {'he': 'ימים מאז 7/10', 'en': 'Days Since Oct 7'}
}

# Add to TRANSLATIONS dictionary
TRANSLATIONS.update({
    'search_config': {'he': 'הגדרות חיפוש', 'en': 'Search Configuration'},
    'start_date': {'he': 'תאריך התחלה', 'en': 'Start Date'},
    'end_date': {'he': 'תאריך סיום', 'en': 'End Date'},
    'status_filter': {'he': 'סינון לפי סטטוס', 'en': 'Filter by Status'},
    'age_filter': {'he': 'סינון לפי גיל', 'en': 'Filter by Age'},
    'search_terms': {'he': 'מילות חיפוש', 'en': 'Search Terms'},
    'key_insights': {'he': 'תובנות מרכזיות', 'en': 'Key Insights'},
    'hostages_summary': {'he': 'סיכום חטופים', 'en': 'Hostages Summary'},
    'vulnerable_groups': {'he': 'קבוצות פגיעות', 'en': 'Vulnerable Groups'},
    'children': {'he': 'ילדים', 'en': 'Children'},
    'elderly': {'he': 'קשישים', 'en': 'Elderly'},
    'cities_affected': {'he': 'ערים נפגעות', 'en': 'Affected Cities'},
    'no_matching_data': {'he': 'לא נמצאו נתונים מתאימים', 'en': 'No matching data found'},
    'social_media_summary': {'he': 'סיכום רשתות חברתיות', 'en': 'Social Media Summary'},
    'total_posts': {'he': 'סה״כ פוסטים', 'en': 'Total Posts'},
    'total_engagement': {'he': 'סה״כ אינטראקציות', 'en': 'Total Engagement'},
    'avg_engagement': {'he': 'ממוצע אינטראקציות', 'en': 'Average Engagement'},
    'engagement_breakdown': {'he': 'פילוח אינטראקציות', 'en': 'Engagement Breakdown'},
    'engagement_rate': {'he': 'אחוז אינטראקציה', 'en': 'Engagement Rate'},
    'posting_patterns': {'he': 'דפוסי פרסום', 'en': 'Posting Patterns'},
    'days_analyzed': {'he': 'ימים שנותחו', 'en': 'Days Analyzed'},
    'posts_per_day': {'he': 'פוסטים ליום', 'en': 'Posts per Day'},
    'peak_day': {'he': 'יום שיא', 'en': 'Peak Day'},
    'data_summary': {'he': 'סיכום נתונים', 'en': 'Data Summary'},
    'no_city_data': {'he': 'אין נתוני ערים', 'en': 'No city data available'},
    'killed': {'he': 'נרצחו', 'en': 'Killed'},
    'unknown': {'he': 'מצב לא ידוע', 'en': 'Unknown Status'},
    'last_update': {'he': 'עדכון אחרון', 'en': 'Last Update'},
    'update_date': {'he': 'תאריך עדכון', 'en': 'Update Date'},
    'days_until_update': {'he': 'ימים עד העדכון', 'en': 'Days Until Update'},
    'data_analysis': {'he': 'ניתוח נתונים', 'en': 'Data Analysis'},
    'trending_hashtags': {'he': 'האשטגים מובילים', 'en': 'Trending Hashtags'},
    'engagement_patterns': {'he': 'דפוסי מעורבות', 'en': 'Engagement Patterns'},
    'view_data': {'he': 'צפייה בנתונים', 'en': 'View Data'},
    'search_posts': {'he': 'חיפוש בפוסטים', 'en': 'Search Posts'},
    'status_and_demographics': {'he': 'סטטוס ודמוגרפיה', 'en': 'Status & Demographics'},
    'timeline_analysis': {'he': 'ניתוח ציר זמן', 'en': 'Timeline Analysis'},
    'detailed_data': {'he': 'נתונים מפורטים', 'en': 'Detailed Data'},
    'key_events': {'he': 'אירועים מרכזיים', 'en': 'Key Events'},
    'filter_data': {'he': 'סינון נתונים', 'en': 'Filter Data'},
    'city_filter': {'he': 'סנן לפי עיר', 'en': 'Filter by City'},
    'search_data': {'he': 'חיפוש בנתונים', 'en': 'Search Data'},
    'search_names': {'he': 'חיפוש שמות', 'en': 'Search Names'},
    'data_source_info': {'he': 'מקור המידע', 'en': 'Data Source'},
    'dataset_stats': {'he': 'סטטיסטיקות המאגר', 'en': 'Dataset Statistics'},
    'update_info': {'he': 'מידע על עדכונים', 'en': 'Update Information'},
    'source_verified': {'he': 'מקור מאומת', 'en': 'Verified Source'},
    'source_official': {'he': 'מקור רשמי', 'en': 'Official Source'},
    'source_realtime': {'he': 'מקור בזמן אמת', 'en': 'Real-time Source'},
    'total_records': {'he': 'סך הכל רשומות', 'en': 'Total Records'},
    'date_range': {'he': 'טווח תאריכים', 'en': 'Date Range'},
    'view_source': {'he': 'צפייה במקור', 'en': 'View Source'},
    'source_reliability': {'he': 'אמינות המקור', 'en': 'Source Reliability'},
    'high_reliability': {'he': 'אמינות גבוהה', 'en': 'High Reliability'},
    'medium_reliability': {'he': 'אמינות בינונית', 'en': 'Medium Reliability'},
    'update_frequency': {'he': 'תדירות עדכון', 'en': 'Update Frequency'}
})

def get_translation(key: str, lang: str) -> str:
    """Get translation for a key in specified language"""
    return TRANSLATIONS.get(key, {}).get(lang, key)

def clean_hostage_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and validate hostage data"""
    try:
        return {
            'name': str(data.get('name', 'Unknown')),
            'age': int(data.get('age', -1)),
            'location_taken': str(data.get('location_taken', 'Unknown')),
            'status': str(data.get('status', 'Unknown')),
            'days_in_captivity': int(data.get('days_in_captivity', -1)),
            'capture_date': data.get('capture_date', '2023-10-07')
        }
    except Exception as e:
        logger.error(f"Error cleaning hostage data: {str(e)}")
        return {}

def validate_data_source(source: str) -> bool:
    """Validate data source type"""
    return source in ['gov', 'csv', 'api']

def calculate_days_in_captivity(capture_date: str) -> int:
    """Calculate days in captivity"""
    try:
        capture = datetime.strptime(capture_date, '%Y-%m-%d')
        return (datetime.now() - capture).days
    except:
        return -1