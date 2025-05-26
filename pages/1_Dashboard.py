"""
Dashboard page for the BrainVenture application.
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.app_config import APP_CONFIG, FEATURE_FLAGS
from config.content_config import load_course_structure, load_neuroleader_types
from components.navigation import sidebar_navigation, page_header
from utils.ui import setup_page, card
from utils.helpers import load_user_data

def main():
    """
    Main function for the Dashboard page.
    """
    # Setup page
    setup_page(
        page_title=f"Dashboard | {APP_CONFIG['app_name']}",
        page_icon=APP_CONFIG["app_icon"],
        layout="wide"
    )
    
    # Display sidebar navigation
    sidebar_navigation()
    
    # Page header
    page_header(
        title="Dashboard",
        description="Witaj w panelu zarządzania Twoim rozwojem neuroprzywódczym",
        icon="🏠"
    )
    
    # Load user data
    user_id = "default_user"  # In a real app, this would come from authentication
    user_data = load_user_data(user_id)
    
    # Welcome message
    st.markdown(f"""
    # Witaj, {user_data.get('profile', {}).get('display_name', 'Użytkowniku')}!
    Twój osobisty rozwój neuroprzywódczy w jednym miejscu.
    """)
    
    # Quick actions
    st.subheader("Szybki Start")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🔍 Poznaj Swój Typ
        Odkryj swój styl przywództwa i neurobiologiczne podstawy Twoich zachowań.
        """)
        if st.button("Zrób Test", key="test_button", use_container_width=True):
            st.switch_page("pages/2_Typy_Neurolidera.py")
    
    with col2:
        st.markdown("""
        ### 📚 Zacznij Kurs
        Rozpocznij swoją podróż do bardziej świadomego przywództwa.
        """)
        if st.button("Zobacz Lekcje", key="course_button", use_container_width=True):
            st.switch_page("pages/3_Struktura_Kursu.py")
    
    with col3:
        st.markdown("""
        ### 📊 Śledź Postępy
        Sprawdź swój rozwój i zaplanuj kolejne kroki.
        """)
        if st.button("Mój Profil", key="profile_button", use_container_width=True):
            st.switch_page("pages/4_Profil.py")
    
    # User progress overview
    st.subheader("Twoje Postępy")
    
    # Calculate progress
    completed_lessons = user_data.get("progress", {}).get("completed_lessons", [])
    progress_percentage = 30  # For MVP, hardcoded at 30%
    
    st.progress(progress_percentage / 100, text=f"Ukończono {progress_percentage}% kursu")
    
    # Latest activity and next recommended lesson
    st.markdown("**Ostatnia aktywność:** Lekcja: Co to jest neuroprzywództwo?")
    st.markdown("**Następna lekcja:** Mózg lidera – struktura i funkcje")
    
    # Show continue button
    if st.button("Kontynuuj Naukę", use_container_width=True):
        st.switch_page("pages/3_Struktura_Kursu.py")
    
    # Featured content section
    st.subheader("Polecane Materiały")
    
    featured_col1, featured_col2 = st.columns(2)
    with featured_col1:
        card(
            title="Neurobiologia przywództwa",
            content="""
            Przywództwo to nie tylko umiejętności miękkie - to także procesy neurobiologiczne zachodzące w Twoim mózgu.
            Dowiedz się, jak Twój mózg podejmuje decyzje i jak możesz wspierać te procesy.
            """,
            icon="🧠",
            color=APP_CONFIG["theme_color"]
        )
    
    with featured_col2:
        card(
            title="Odkryj swój typ neurolidera",
            content="""
            Czy jesteś Neuroempatą, Neuroinnowatorem, a może Neuroreaktorem?
            Zrób test i poznaj swój dominujący styl przywództwa z perspektywy neurobiologicznej.
            """,
            icon="🔍",
            color=APP_CONFIG["secondary_color"]
        )
    
    # Neuroleader types overview
    st.subheader("Typy Neuroleaderów")
    
    # Load neuroleader types
    neuroleader_types = load_neuroleader_types()
    
    # Display types in a grid
    cols = st.columns(3)
    for i, ntype in enumerate(neuroleader_types[:6]):  # Show first 6 types
        with cols[i % 3]:
            type_icon = ntype.get("icon", "🧠")
            type_name = ntype.get("name", "Typ Neurolidera")
            type_desc = ntype.get("short_description", "")
            
            st.markdown(f"### {type_icon} {type_name}")
            st.markdown(type_desc)
            
            if st.button(f"Dowiedz się więcej o {ntype.get('id', '')}", key=f"learn_{ntype.get('id', '')}", use_container_width=True):
                # Store the selected type in session state
                st.session_state["selected_type"] = ntype.get("id", "")
                st.switch_page("pages/2_Typy_Neurolidera.py")
    
    # Latest achievements
    st.subheader("Najnowsze Osiągnięcia")
    achievement_col1, achievement_col2, achievement_col3 = st.columns(3)
    
    with achievement_col1:
        st.markdown("🏆 **Pierwsza Lekcja** - Rozpocząłeś swoją drogę z neuroprzywództwem!")
    
    with achievement_col2:
        st.markdown("📋 **Kwestionariusz** - Wykonałeś swój pierwszy test typologii!")
    
    with achievement_col3:
        st.markdown("📊 **Analityk** - Przeanalizowałeś swój profil neuroliderski!")

if __name__ == "__main__":
    main()
