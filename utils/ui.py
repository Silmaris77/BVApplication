"""
UI utilities for the BrainVenture application.
"""

import streamlit as st
import random
import os
from config.app_config import APP_CONFIG

def setup_page(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="auto"):
    """
    Configure the Streamlit page settings.
    
    Args:
        page_title (str): The title of the page.
        page_icon (str): The page icon (emoji or URL).
        layout (str): The layout of the page ("centered" or "wide").
        initial_sidebar_state (str): Initial state of the sidebar ("auto", "expanded", "collapsed").
    """
    if page_title is None:
        page_title = APP_CONFIG["app_name"]
    
    if page_icon is None:
        page_icon = APP_CONFIG["app_icon"]
      # Validate layout parameter (must be one of the accepted literals)
    if layout == "wide":
        layout_value = "wide"
    else:
        layout_value = "centered"
    
    # Validate initial_sidebar_state parameter (must be one of the accepted literals)
    if initial_sidebar_state == "expanded":
        sidebar_state = "expanded"
    elif initial_sidebar_state == "collapsed":
        sidebar_state = "collapsed"
    else:
        sidebar_state = "auto"
    
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout_value,
        initial_sidebar_state=sidebar_state,
    )
    
    # Apply CSS
    apply_custom_css()
    
    # Apply JavaScript
    apply_custom_js()

def apply_custom_js():
    """Apply custom JavaScript to the Streamlit app."""
    # Include external JS file if it exists
    js_path = os.path.join("static", "js", "brainventure.js")
    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as js_file:
            js_content = js_file.read()
            html = f'<script>{js_content}</script>'
            st.markdown(html, unsafe_allow_html=True)

def apply_custom_css():
    """Apply custom CSS to the Streamlit app."""
    # Include external CSS file if it exists
    css_path = os.path.join("static", "css", "custom.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as css_file:
            st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)
    
    # Define additional inline CSS for Material Design 3 styling
    custom_css = f"""
    <style>
        /* Base Styles */
        body {{
            font-family: {APP_CONFIG['font_family_body']};
            color: {APP_CONFIG['text_color']};
            background-color: {APP_CONFIG['background_color']};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: {APP_CONFIG['font_family_headers']};
            font-weight: 500;
        }}
        
        /* Card Styles */
        .stCard {{
            background-color: {APP_CONFIG['card_background']};
            border-radius: 16px;
            box-shadow: {APP_CONFIG['card_shadow']};
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stCard:hover {{
            transform: translateY(-5px);
            box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.15);
        }}
        
        /* Button Styles */
        .stButton > button {{
            border-radius: 20px;
            padding: 0.5rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        /* Primary Button */
        .primary-btn {{
            background-color: {APP_CONFIG['theme_color']};
            color: white;
        }}
        
        /* Secondary Button */
        .secondary-btn {{
            background-color: {APP_CONFIG['secondary_color']};
            color: white;
        }}
        
        /* Accent Button */
        .accent-btn {{
            background-color: {APP_CONFIG['accent_color']};
            color: white;
        }}
        
        /* Progress Bar */
        .stProgress > div > div > div > div {{
            background-color: {APP_CONFIG['theme_color']};
        }}
        
        /* Sidebar */
        .css-1d391kg, .css-12oz5g7 {{
            background-color: #f9f9f9;
            border-right: 1px solid #e0e0e0;
        }}
        
        /* Metrics */
        .stMetric {{
            background-color: {APP_CONFIG['card_background']};
            border-radius: 12px;
            padding: 1rem;
            box-shadow: {APP_CONFIG['card_shadow']};
        }}
        
        /* Sections */
        .section {{
            padding: 1.5rem 0;
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 1.5rem;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        /* Badge styles */
        .badge {{
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 16px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .badge-primary {{
            background-color: {APP_CONFIG['theme_color']};
            color: white;
        }}
        
        .badge-secondary {{
            background-color: {APP_CONFIG['secondary_color']};
            color: white;
        }}
        
        .badge-accent {{
            background-color: {APP_CONFIG['accent_color']};
            color: white;
        }}
        
        /* Custom Card Grid */
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            grid-gap: 1.5rem;
        }}
        
        /* Avatar */
        .avatar {{
            border-radius: 50%;
            object-fit: cover;
        }}
        
        /* Custom Progress Bar */
        .custom-progress {{
            height: 10px;
            background-color: #e0e0e0;
            border-radius: 5px;
            margin: 10px 0;
        }}
        
        .custom-progress-bar {{
            height: 100%;
            border-radius: 5px;
            background-color: {APP_CONFIG['theme_color']};
            transition: width 0.3s ease;
        }}
    </style>
    """
    
    # Apply the CSS
    st.markdown(custom_css, unsafe_allow_html=True)

def card(title, content, icon=None, footer=None, color=None, is_achievement=False, locked=False):
    """
    Display a card with content.
    
    Args:
        title (str): Card title.
        content (str): Card content.
        icon (str, optional): Emoji or image icon.
        footer (str, optional): Footer text to display at bottom of card.
        color (str, optional): Color for the card border or accent (hex code or color name).
        is_achievement (bool, optional): Whether this card represents an achievement.
        locked (bool, optional): Whether this achievement is locked.
    """
    card_style = "border: 1px solid #ddd; border-radius: 10px; padding: 20px; height: 100%;"
    
    # Apply custom color if provided
    if color:
        card_style = f"border: 1px solid {color}; border-radius: 10px; padding: 20px; height: 100%; border-left: 5px solid {color};"
    
    if locked:
        card_style += " opacity: 0.7;"
    
    with st.container():
        st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
        
        # Title row with icon
        title_style = "margin: 0;"
        if color:
            title_style = f"margin: 0; color: {color};"
            
        if icon:
            col1, col2 = st.columns([1, 9])
            with col1:
                st.markdown(f"<h2 style='margin: 0;'>{icon}</h2>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<h3 style='{title_style}'>{title}</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='{title_style}'>{title}</h3>", unsafe_allow_html=True)
        
        # Content
        st.markdown(content)
        
        # Footer if provided
        if footer:
            st.markdown(f"<div style='color: #666; font-size: 0.8em; margin-top: 10px;'>{footer}</div>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

def simple_badge(text, badge_type="primary"):
    """
    Create a styled simple badge with predefined colors.
    
    Args:
        text (str): The text for the badge.
        badge_type (str): Type of badge ('primary', 'secondary', 'accent').
    
    Returns:
        str: HTML for the badge.
    """
    color_map = {
        "primary": APP_CONFIG["theme_color"],
        "secondary": APP_CONFIG["secondary_color"],
        "accent": APP_CONFIG["accent_color"],
    }
    
    color = color_map.get(badge_type, APP_CONFIG["theme_color"])
    
    badge_html = f"""
    <span style="
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 500;
        background-color: {color};
        color: white;
    ">
        {text}
    </span>
    """
    
    return badge_html

def progress_bar(value, max_value=100, text=None, min_value=0, color=None):
    """
    Display a customized progress bar with optional text.
    
    Args:
        value (float): The current progress value (between min_value and max_value).
        max_value (float, optional): The maximum value of the progress bar. Defaults to 100.
        text (str, optional): Text to display on the progress bar. Defaults to None.
        min_value (float, optional): The minimum value of the progress bar. Defaults to 0.
        color (str, optional): Color of the progress bar. Defaults to the theme color.
    """
    # Normalize the value to be between 0 and 1
    normalized_value = (value - min_value) / (max_value - min_value) if max_value > min_value else 0
    normalized_value = max(0, min(1, normalized_value))  # Clamp between 0 and 1
    
    # Use Streamlit's progress bar
    if text:
        return st.progress(normalized_value, text=text)
    else:
        return st.progress(normalized_value)

def tabs(tab_items):
    """
    Create styled tabs for content organization.
    
    Args:
        tab_items (list): Either:
            - A list of tab names (strings)
            - A list of (tab_name, tab_content_function) tuples where:
                - tab_name (str): The name of the tab
                - tab_content_function (callable): Function to call when the tab is selected
            
    Returns:
        The selected tab name or index.
    """
    # Check if tab_items is a list of strings or a list of tuples
    if tab_items and isinstance(tab_items[0], str):
        # It's a list of tab names (strings)
        tab_labels = tab_items
        tabs = st.tabs(tab_labels)
        # Return the selected tab name
        active_tab_index = st.session_state.get("active_tab", 0)
        if 0 <= active_tab_index < len(tab_labels):
            return tab_labels[active_tab_index]
        return tab_labels[0] if tab_labels else None
    else:
        # It's a list of (tab_name, tab_content_function) tuples
        tab_labels = [item[0] for item in tab_items]
        tabs = st.tabs(tab_labels)
        
        # Display content for each tab
        for i, (_, content_func) in enumerate(tab_items):
            with tabs[i]:
                content_func()
        
        return st.session_state.get("active_tab", 0)

def avatar(name, size=100, image_path=None):
    """
    Display a user avatar, either from image or generated from initials.
    
    Args:
        name (str): User name (used for generating initials avatar if no image)
        size (int): Size of the avatar in pixels
        image_path (str, optional): Path to the avatar image
    """
    import hashlib
    
    if image_path and os.path.exists(image_path):
        # Use the actual image if available
        st.image(image_path, width=size)
    else:
        # Generate an avatar with initials on a colored background
        if not name:
            name = "User"
            
        # Get initials (up to 2 characters)
        initials = "".join([word[0].upper() for word in name.split()[:2]])
        if not initials:
            initials = name[0].upper()
        
        # Generate a consistent background color based on the name
        hash_object = hashlib.md5(name.encode())
        hash_hex = hash_object.hexdigest()
        hue = int(hash_hex[:2], 16) / 255.0  # Use first byte for hue (0-1)
        
        # Use HSL color model for better control of lightness
        import colorsys
        rgb = colorsys.hls_to_rgb(hue, 0.5, 0.7)  # Lightness 0.5, Saturation 0.7
        r, g, b = [int(255 * c) for c in rgb]
        bg_color = f"rgb({r},{g},{b})"
        
        # Create CSS for the avatar
        avatar_css = f"""
        <div style="
            width: {size}px;
            height: {size}px;
            border-radius: 50%;
            background-color: {bg_color};
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: {size // 3}px;
            font-weight: bold;
        ">
            {initials}
        </div>
        """
        
        st.markdown(avatar_css, unsafe_allow_html=True)

def badge(text, color=None, icon=None, size="small"):
    """
    Display a badge with optional icon.
    
    Args:
        text (str): Text to display on the badge
        color (str, optional): Badge color (hex code or color name)
        icon (str, optional): Icon to display (emoji or icon name)
        size (str, optional): Size of badge ("small", "medium", "large")
    """
    # Default color if none provided
    if color is None:
        color = "#6c757d"  # Bootstrap secondary color
        
    # Size classes
    size_class = {
        "small": "0.75em",
        "medium": "0.9em",
        "large": "1em"
    }.get(size, "0.75em")
    
    # Padding based on size
    padding = {
        "small": "0.25em 0.5em",
        "medium": "0.35em 0.65em",
        "large": "0.5em 0.85em"
    }.get(size, "0.25em 0.5em")
    
    # Create the HTML
    icon_html = f"{icon} " if icon else ""
    badge_html = f"""
    <span style="
        display: inline-block;
        padding: {padding};
        font-size: {size_class};
        font-weight: 500;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.25rem;
        color: white;
        background-color: {color};
    ">
        {icon_html}{text}
    </span>
    """
    
    st.markdown(badge_html, unsafe_allow_html=True)

def tag_badge(tag_text, color=None):
    """
    Create an HTML badge specifically for tags with a hash symbol (#).
    
    Args:
        tag_text (str): The text to display on the tag badge.
        color (str, optional): The background color of the badge. Defaults to a random color.
    
    Returns:
        str: HTML string representing the tag badge.
    """
    # Define a list of pastel colors to use for tags if no color is provided
    tag_colors = [
        "#E9F5DB", "#CFE1B9", "#B5C99A", "#97A97C", "#87986A",  # Greens
        "#EAD2AC", "#E6B89C", "#C9ADA1", "#9A8C98", "#4A4E69",  # Browns
        "#E0FBFC", "#C2DFE3", "#9DB4C0", "#5C6B73", "#253237",  # Blues
        "#FFCDB2", "#FFB4A2", "#E5989B", "#B5838D", "#6D6875",  # Pinks
    ]
    
    # Use provided color or pick a consistent color based on the tag text
    if color is None:
        # Use a hash of the tag text to pick a consistent color for the same tag
        tag_hash = sum(ord(c) for c in tag_text)
        color = tag_colors[tag_hash % len(tag_colors)]
    
    # Calculate a contrasting text color (dark for light backgrounds, light for dark backgrounds)
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    text_color = "#000000" if luminance > 0.5 else "#FFFFFF"
    
    # Create the HTML for the badge
    badge_html = f"""
    <span style="
        display: inline-block;
        background-color: {color};
        color: {text_color};
        padding: 2px 8px;
        margin-right: 8px;
        margin-bottom: 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 500;
    ">#{tag_text}</span>
    """
    
    return badge_html
