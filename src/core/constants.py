# Menu structure
MENU_ITEMS = {
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

# Chart colors
CHART_COLORS = {
    'primary': '#1f77b4',
    'success': '#51cf66',
    'danger': '#ff6b6b',
    'warning': '#ffd43b',
    'info': '#4dabf7'
}

# Status mappings
STATUS_MAPPINGS = {
    'in hamas captivity': 'Held',
    'released': 'Released',
    'deceased': 'Deceased',
    'status unknown': 'Unknown'
}

# Age group bins
AGE_GROUPS = [
    (0, 12, 'Child'),
    (13, 18, 'Teen'),
    (19, 30, 'Young Adult'),
    (31, 50, 'Adult'),
    (51, 70, 'Senior'),
    (71, 100, 'Elderly')
] 