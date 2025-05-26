"""
Application configuration settings.
"""

APP_CONFIG = {
    "app_name": "BrainVenture: Kurs Neuroprzywództwa",
    "app_icon": "🧠",
    "app_description": "Odkryj, jak neurobiologia może pomóc Ci stać się skuteczniejszym liderem",
    "version": "0.1.0 (MVP)",
    "theme_color": "#3498db",
    "secondary_color": "#2ecc71",
    "accent_color": "#e74c3c",
    "text_color": "#34495e",
    "background_color": "#f5f5f5",
    "card_background": "#ffffff",
    "card_shadow": "0px 4px 12px rgba(0, 0, 0, 0.1)",
    "font_family_headers": "Roboto, sans-serif",
    "font_family_body": "Roboto, sans-serif",
}

FEATURE_FLAGS = {
    "enable_test": True,
    "enable_course_view": True,
    "enable_dashboard": True,
    "enable_profile": True,
    "enable_blog": True,
    "enable_gamification": True,
    "enable_analytics": False,  # Not in MVP
    "enable_certificate": False,  # Not in MVP
    "enable_social_sharing": False,  # Not in MVP
    "enable_advanced_reporting": False,  # Not in MVP
}

APP_PATHS = {
    "content_dir": "data/content",
    "user_files_dir": "data/user_files",
    "static_dir": "static",
    "images_dir": "static/images",
    "neuroleader_types_json": "data/content/neuroleader_types.json",
    "neuroleader_test_json": "data/content/neuroleader_type_test.json",
    "course_structure_json": "data/content/course_structure.json",
}
