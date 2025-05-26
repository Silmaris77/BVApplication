"""
Navigation components for the BrainVenture application.
"""

import streamlit as st
import os
from config.app_config import APP_CONFIG, FEATURE_FLAGS
from utils.ui import avatar

def sidebar_navigation():
    """
    Display the navigation sidebar.
    """
    with st.sidebar:
        # User profile section
        if "user" not in st.session_state:
            st.session_state["user"] = {
                "id": "default_user",  # In a real app, this would be from authentication
                "name": "Demo User",
                "progress": 30,  # Example progress percentage
                "type": "neuroempata"  # Example neuroleader type
            }
        
        user = st.session_state["user"]
        
        # User profile summary
        st.markdown("### Twój Profil")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display user avatar
            avatar(user["name"], size=60)
        
        with col2:
            st.markdown(f"**{user['name']}**")
            st.markdown(f"Postęp: **{user['progress']}%**")
            if user.get("type"):
                st.markdown(f"Typ: **{user['type'].capitalize()}**")
        
        st.divider()
        
        # Main navigation menu
        st.markdown("### Nawigacja")
        
        # Dashboard
        if FEATURE_FLAGS["enable_dashboard"]:
            dashboard_icon = "🏠"
            if st.button(f"{dashboard_icon} Dashboard", use_container_width=True):
                st.switch_page("app.py")  # Main dashboard page
        
        # Test type
        if FEATURE_FLAGS["enable_test"]:
            test_icon = "🧩"
            if st.button(f"{test_icon} Typy Neurolidera", use_container_width=True):
                st.switch_page("pages/2_Typy_Neurolidera.py")
        
        # Course structure
        if FEATURE_FLAGS["enable_course_view"]:
            course_icon = "📚"
            if st.button(f"{course_icon} Struktura Kursu", use_container_width=True):
                st.switch_page("pages/3_Struktura_Kursu.py")
        
        # User profile
        if FEATURE_FLAGS["enable_profile"]:
            profile_icon = "👤"
            if st.button(f"{profile_icon} Profil", use_container_width=True):
                st.switch_page("pages/4_Profil.py")
        
        # Blog
        if FEATURE_FLAGS["enable_blog"]:
            blog_icon = "📰"
            if st.button(f"{blog_icon} Zasoby", use_container_width=True):
                st.switch_page("pages/5_Zasoby.py")
        
        # Settings
        settings_icon = "⚙️"
        if st.button(f"{settings_icon} Ustawienia", use_container_width=True):
            st.session_state["show_settings"] = True
        
        st.divider()
        
        # App info footer
        st.markdown(f"**{APP_CONFIG['app_name']}**")
        st.markdown(f"Wersja: {APP_CONFIG['version']}")
        
        # Show settings modal if requested
        if st.session_state.get("show_settings", False):
            show_settings_modal()

def show_settings_modal():
    """
    Display a settings modal overlay.
    """
    with st.sidebar.expander("⚙️ Ustawienia", expanded=True):
        st.markdown("### Ustawienia")
        
        # Theme settings
        theme = st.selectbox(
            "Motyw",
            ["Jasny", "Ciemny", "Systemowy"],
            index=0
        )
        
        # Notification settings
        notifications = st.checkbox("Powiadomienia", value=True)
        
        # Language settings (for future implementation)
        language = st.selectbox(
            "Język",
            ["Polski", "English"],
            index=0,
            disabled=True
        )
        
        # Save button
        if st.button("Zapisz ustawienia", use_container_width=True):
            # In a real app, we would save these settings to user preferences
            st.session_state["settings"] = {
                "theme": theme.lower(),
                "notifications": notifications,
                "language": language
            }
            st.success("Ustawienia zostały zapisane.")
            # Close the modal after saving
            st.session_state["show_settings"] = False
        
        # Cancel button
        if st.button("Anuluj", use_container_width=True):
            st.session_state["show_settings"] = False

def page_header(title, description=None, icon=None):
    """
    Display a consistent page header.
    
    Args:
        title (str): Page title
        description (str, optional): Page description
        icon (str, optional): Emoji icon
    """
    if icon:
        st.markdown(f"# {icon} {title}")
    else:
        st.markdown(f"# {title}")
    
    if description:
        st.markdown(description)
    
    st.divider()

def breadcrumbs(items):
    """
    Display breadcrumb navigation.
    
    Args:
        items (list): List of (label, url) tuples
    """
    breadcrumb_html = '<div style="margin-bottom: 1rem; font-size: 0.8rem;">'
    
    for i, (label, url) in enumerate(items):
        if i > 0:
            breadcrumb_html += ' &gt; '
        
        if url and i < len(items) - 1:
            breadcrumb_html += f'<a href="{url}" target="_self">{label}</a>'
        else:
            breadcrumb_html += f'<span style="color: #666;">{label}</span>'
    
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)
