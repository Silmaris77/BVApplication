"""
User Profile page for the BrainVenture application.
"""

import streamlit as st
import os
import sys
import json
import pandas as pd
from datetime import datetime

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.app_config import APP_CONFIG, FEATURE_FLAGS
from components.navigation import sidebar_navigation
from components.user_profile import (
    user_profile_header, user_achievements, user_progress_stats,
    edit_user_profile_form, user_activity_timeline
)
from utils.ui import setup_page, card, tabs
from utils.helpers import load_user_data, save_user_data

def main():
    """Main function for the User Profile page."""
    # Setup page configuration
    setup_page(
        page_title=f"Profil | {APP_CONFIG['app_name']}",
        page_icon=APP_CONFIG["app_icon"],
        layout="wide",
    )
    
    # Display sidebar navigation
    sidebar_navigation()
    
    # Page header
    st.title("🧑‍💼 Twój Profil")
    
    # Load user data
    user_data = load_user_data()
    
    # Display user profile header with avatar and basic info
    user_profile_header(user_data)
    
    # Create tabs for different profile sections
    tab_options = ["Postęp", "Osiągnięcia", "Aktywność", "Ustawienia"]
    selected_tab = tabs(tab_options)
    
    # Display tab contents based on selection
    if selected_tab == "Postęp":
        display_progress_tab(user_data)
    elif selected_tab == "Osiągnięcia":
        display_achievements_tab(user_data)
    elif selected_tab == "Aktywność":
        display_activity_tab(user_data)
    elif selected_tab == "Ustawienia":
        display_settings_tab(user_data)

def display_progress_tab(user_data):
    """
    Display user progress statistics.
    
    Args:
        user_data (dict): User data dictionary.
    """
    st.header("Twój Postęp w Nauce")
    
    # Display progress stats
    user_progress_stats(user_data)
    
    # Display recommended next steps
    st.subheader("Zalecane Następne Kroki")
    
    # Get user's last completed lesson
    completed_lessons = user_data.get("progress", {}).get("completed_lessons", [])
    
    # Recommend next content based on last activity
    if completed_lessons:
        col1, col2 = st.columns(2)
        
        with col1:
            card(
                title="Kontynuuj Naukę",
                content="Lekcja: Mózg lidera – struktura i funkcje",
                icon="📚",
                footer="Moduł 1, Lekcja 3 • Czas: 15 min"
            )
        
        with col2:
            card(
                title="Praktyczne Ćwiczenie",
                content="Identyfikacja własnych wyzwań jako lidera",
                icon="✍️",
                footer="Zwiększa efektywność nauki o 40%"
            )
    else:
        st.info("Rozpocznij kurs, aby otrzymać spersonalizowane rekomendacje.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Rozpocznij Kurs", key="start_course")
        with col2:
            st.button("Zrób Test Typu Neurolidera", key="take_test")

def display_achievements_tab(user_data):
    """
    Display user achievements.
    
    Args:
        user_data (dict): User data dictionary.
    """
    st.header("Twoje Osiągnięcia")
    user_achievements(user_data)
    
    # Display locked achievements as motivation
    st.subheader("Odblokuj Więcej")
    
    locked_col1, locked_col2, locked_col3 = st.columns(3)
    
    with locked_col1:
        card(
            title="Mistrz Wiedzy",
            content="Ukończ wszystkie lekcje w module 1",
            icon="🔒",
            is_achievement=True,
            locked=True
        )
    
    with locked_col2:
        card(
            title="Społeczny Strateg",
            content="Ukończ wszystkie lekcje o zarządzaniu zespołem",
            icon="🔒",
            is_achievement=True,
            locked=True
        )
        
    with locked_col3:
        card(
            title="Neuro-Ekspert",
            content="Zdobądź minimalnie 80% w teście końcowym",
            icon="🔒",
            is_achievement=True,
            locked=True
        )

def display_activity_tab(user_data):
    """
    Display user activity timeline.
    
    Args:
        user_data (dict): User data dictionary.
    """
    st.header("Twoja Aktywność")
    
    # Show activity timeline
    user_activity_timeline(user_data)
    
    # Display statistics
    st.subheader("Statystyki Aktywności")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        activities = user_data.get("activity", [])
        total_activities = len(activities) if activities else 0
        st.metric(label="Całkowita Aktywność", value=total_activities)
    
    with stats_col2:
        # Calculate streak (consecutive days with activity)
        streak = user_data.get("stats", {}).get("current_streak", 0)
        st.metric(label="Seria Dni", value=streak)
        
    with stats_col3:
        # Get total time spent in minutes
        time_spent = user_data.get("stats", {}).get("total_time_spent", 0)
        hours = time_spent // 60
        minutes = time_spent % 60
        st.metric(label="Czas Nauki", value=f"{hours}h {minutes}min")

def display_settings_tab(user_data):
    """
    Display and edit user settings.
    
    Args:
        user_data (dict): User data dictionary.
    """
    st.header("Ustawienia Profilu")
    
    # Display edit profile form
    updated_profile = edit_user_profile_form(user_data)
    
    if updated_profile:
        # Update user data
        user_data["profile"] = updated_profile
        user_data["updated_at"] = datetime.now().isoformat()
        
        # Save updated user data
        save_user_data(user_data)
        st.success("Profil zaktualizowany pomyślnie!")
        
    # Notification settings
    st.subheader("Powiadomienia")
    
    notify_new_content = st.checkbox(
        "Powiadomienia o nowych treściach",
        value=user_data.get("settings", {}).get("notifications", {}).get("new_content", True)
    )
    
    notify_achievements = st.checkbox(
        "Powiadomienia o osiągnięciach",
        value=user_data.get("settings", {}).get("notifications", {}).get("achievements", True)
    )
    
    # Save notification settings if changed
    if st.button("Zapisz Ustawienia Powiadomień"):
        if "settings" not in user_data:
            user_data["settings"] = {}
        if "notifications" not in user_data["settings"]:
            user_data["settings"]["notifications"] = {}
            
        user_data["settings"]["notifications"]["new_content"] = notify_new_content
        user_data["settings"]["notifications"]["achievements"] = notify_achievements
        user_data["updated_at"] = datetime.now().isoformat()
        
        # Save updated user data
        save_user_data(user_data)
        st.success("Ustawienia powiadomień zaktualizowane!")
    
    # Display data export option
    st.subheader("Eksport Danych")
    if st.button("Eksportuj Dane Profilu"):
        st.json(user_data)
        st.download_button(
            label="Pobierz jako JSON",
            data=json.dumps(user_data, indent=2, default=str),
            file_name="moj_profil_brainventure.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
