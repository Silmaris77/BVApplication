import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from config.app_config import APP_CONFIG
from config.security_config import setup_security
from utils.ui import setup_page
from components.navigation import sidebar_navigation

def main():
    """
    Main function that sets up the BrainVenture application.
    """
    # Setup page configuration, security, and other initial settings
    setup_page(
        page_title=APP_CONFIG["app_name"],
        page_icon=APP_CONFIG["app_icon"],
        layout="wide",
    )
    
    # Setup security headers for CSP compliance
    setup_security()
    
    # Set up application header
    logo_loaded = False
    try:
        # Get the absolute base path of the application
        base_path = os.path.abspath(os.path.dirname(__file__))
        
        # Try to load the SVG version first (better quality)
        logo_svg_path = os.path.join(base_path, "static", "images", "brainventure_logo.svg")
        if os.path.exists(logo_svg_path):
            st.image(logo_svg_path, width=300)
            logo_loaded = True
        else:
            # Fall back to PNG if SVG doesn't exist
            logo_png_path = os.path.join(base_path, "static", "images", "brainventure_logo.png") 
            if os.path.exists(logo_png_path):
                st.image(logo_png_path, width=300)
                logo_loaded = True
            else:
                print(f"Logo files not found at: {logo_svg_path} or {logo_png_path}")
    except Exception as e:
        print(f"Error loading logo image: {str(e)}")
    
    # Display app name - either as main header or as secondary if logo was loaded
    if not logo_loaded:
        st.markdown(f"# {APP_CONFIG['app_name']}")
    else:
        st.markdown(f"## {APP_CONFIG['app_name']}")
        
    st.markdown(f"{APP_CONFIG['app_description']}")
    
    # Display sidebar navigation
    sidebar_navigation()

    # Main page content (Dashboard)
    st.header("🧠 Odkryj Neuro-Liderstwo")
    
    # Quick actions
    st.subheader("Szybki Start")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🔍 Poznaj Swój Typ
        Odkryj swój styl przywództwa i neurobiologiczne podstawy Twoich zachowań.
        """)
        st.button("Zrób Test", key="test_button")
    
    with col2:
        st.markdown("""
        ### 📚 Zacznij Kurs
        Rozpocznij swoją podróż do bardziej świadomego przywództwa.
        """)
        st.button("Zobacz Lekcje", key="course_button")
    
    with col3:
        st.markdown("""
        ### 📊 Śledź Postępy
        Sprawdź swój rozwój i zaplanuj kolejne kroki.
        """)
        st.button("Mój Profil", key="profile_button")
    
    # Featured content
    st.subheader("Polecane Materiały")
    
    featured_col1, featured_col2 = st.columns(2)
    with featured_col1:
        st.markdown("""
        #### Najnowsza Lekcja
        **Jak emocje wpływają na decyzje liderów?**
        
        Poznaj neurobiologiczne podstawy podejmowania decyzji w kontekście emocji.
        """)
        st.button("Kontynuuj Naukę", key="continue_button")
    
    with featured_col2:
        st.markdown("""
        #### Blog
        **5 technik zarządzania stresem w oparciu o neurobiologię**
        
        Praktyczne wskazówki jak wykorzystać wiedzę o mózgu do lepszego radzenia sobie ze stresem.
        """)
        st.button("Czytaj", key="read_button")
    
    # Progress overview
    st.subheader("Twoje Postępy")
    st.progress(30, text="Ukończono 30% kursu")
    
    st.markdown("**Ostatnia aktywność:** Lekcja: Co to jest neuroprzywództwo?")
    st.markdown("**Następna lekcja:** Mózg lidera – struktura i funkcje")
    
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
