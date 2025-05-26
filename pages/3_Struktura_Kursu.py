"""
Course Structure page for the BrainVenture application.
"""

import streamlit as st
import os
import sys
import json
import pandas as pd

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.app_config import APP_CONFIG
from config.content_config import load_course_structure
from components.navigation import sidebar_navigation, page_header, breadcrumbs
from utils.ui import setup_page, card, progress_bar
from utils.helpers import load_user_data, save_user_data, award_achievement, calculate_progress

def display_course_structure():
    """
    Display the complete course structure.
    """
    st.markdown("# Struktura Kursu")
    st.markdown("""
    Kurs składa się z 5 bloków tematycznych, 15 modułów i 150 lekcji.
    Każdy blok koncentruje się na innym aspekcie neuroprzywództwa.
    """)
    
    # Load course structure
    course_structure = load_course_structure()
    
    # Load user data to check completed lessons
    user_id = "default_user"  # In a real app, this would come from authentication
    user_data = load_user_data(user_id)
    completed_lessons = user_data.get("progress", {}).get("completed_lessons", [])
    
    # Display course blocks
    for block_index, block in enumerate(course_structure):
        block_title = block.get("title", f"Blok {block_index + 1}")
        block_emoji = block.get("emoji", "📚")
        
        # Count total and completed lessons in this block
        block_total_lessons = 0
        block_completed_lessons = 0
        
        for module_index, module in enumerate(block.get("modules", [])):
            block_total_lessons += len(module.get("lessons", []))
            
            # Count completed lessons in this module
            for lesson_index, _ in enumerate(module.get("lessons", [])):
                lesson_id = f"b{block_index+1}_m{module_index+1}_l{lesson_index+1}"
                if lesson_id in completed_lessons:
                    block_completed_lessons += 1
        
        # Calculate block progress
        if block_total_lessons > 0:
            block_progress = calculate_progress(block_completed_lessons, block_total_lessons)
        else:
            block_progress = 0
        
        # Create an expandable section for each block
        with st.expander(f"{block_emoji} {block_title} ({block_progress}%)", expanded=block_index == 0):
            # Display block description
            st.markdown(f"### {block_emoji} {block_title}")
            
            # Display progress bar for the block
            st.progress(block_progress / 100, text=f"{block_completed_lessons}/{block_total_lessons} lekcji ukończonych")
            
            # Display modules in this block
            for module_index, module in enumerate(block.get("modules", [])):
                module_title = module.get("title", f"Moduł {module_index + 1}")
                
                st.markdown(f"#### {module_title}")
                
                # Create a table for lessons
                lessons_data = []
                for lesson_index, lesson in enumerate(module.get("lessons", [])):
                    lesson_title = lesson.get("title", f"Lekcja {lesson_index + 1}")
                    lesson_id = f"b{block_index+1}_m{module_index+1}_l{lesson_index+1}"
                    
                    # Check if lesson is completed
                    is_completed = lesson_id in completed_lessons
                    status = "✅" if is_completed else "⬜"
                    
                    # Add lesson to table
                    lessons_data.append({
                        "status": status,
                        "lesson": lesson_title,
                        "id": lesson_id
                    })
                
                # Display lessons as a table
                if lessons_data:
                    lessons_df = pd.DataFrame(lessons_data)
                    st.table(lessons_df[["status", "lesson"]])

def display_lesson_content(lesson_id, lesson_title):
    """
    Display the content of a specific lesson.
    
    Args:
        lesson_id (str): Lesson ID in format 'b1_m1_l1'.
        lesson_title (str): Lesson title.
    """
    st.markdown(f"# {lesson_title}")
    
    # In a real app, this would load actual lesson content from a database or files
    # For the MVP, we'll simulate some content
    
    # Display breadcrumb navigation
    parts = lesson_id.split("_")
    block_num = int(parts[0][1:])
    module_num = int(parts[1][1:])
    lesson_num = int(parts[2][1:])
    
    breadcrumbs([
        ("Struktura Kursu", None),
        (f"Blok {block_num}", None),
        (f"Moduł {module_num}", None),
        (lesson_title, None)
    ])
    
    # Simulate lesson content
    st.markdown("""
    ## Cele lekcji
    - Zrozumienie podstawowych koncepcji omawianych w tej lekcji
    - Poznanie praktycznych zastosowań wiedzy
    - Nabycie umiejętności wykorzystania informacji w praktyce przywódczej
    
    ## Wprowadzenie
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, 
    nunc nisl aliquam nunc, vitae aliquam nunc nisl eget nisl. Nullam auctor, nisl eget ultricies tincidunt,
    nunc nisl aliquam nunc, vitae aliquam nunc nisl eget nisl.
    
    ## Główne zagadnienia
    1. Pierwsza kluczowa koncepcja
    2. Druga istotna kwestia
    3. Praktyczne zastosowanie wiedzy
    4. Przykłady z życia liderów
    
    ## Szczegółowa analiza
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, 
    nunc nisl aliquam nunc, vitae aliquam nunc nisl eget nisl. Nullam auctor, nisl eget ultricies tincidunt,
    nunc nisl aliquam nunc, vitae aliquam nunc nisl eget nisl.
    
    ## Podsumowanie
    - Kluczowy punkt pierwszy
    - Istotne odkrycie drugie
    - Praktyczna wskazówka trzecia
    
    ## Zadanie do refleksji
    Zastanów się, jak możesz zastosować poznane koncepcje w swojej codziennej praktyce przywódczej.
    """)
    
    # Lesson navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if lesson_num > 1:
            prev_lesson_id = f"b{block_num}_m{module_num}_l{lesson_num-1}"
            if st.button("← Poprzednia lekcja", use_container_width=True):
                st.session_state["lesson_id"] = prev_lesson_id
                st.session_state["lesson_title"] = f"Lekcja {lesson_num-1}"
                st.rerun()
    
    with col2:
        if st.button("Oznacz jako ukończoną", use_container_width=True):
            # In a real app, this would update the lesson status in the database
            user_id = "default_user"  # In a real app, this would come from authentication
            user_data = load_user_data(user_id)
            
            if "progress" not in user_data:
                user_data["progress"] = {}
            
            if "completed_lessons" not in user_data["progress"]:
                user_data["progress"]["completed_lessons"] = []
            
            if lesson_id not in user_data["progress"]["completed_lessons"]:
                user_data["progress"]["completed_lessons"].append(lesson_id)
                save_user_data(user_data, user_id)
                
                # Award achievement for first completed lesson
                if len(user_data["progress"]["completed_lessons"]) == 1:
                    award_achievement(
                        user_id,
                        "Pierwszy Krok",
                        "Ukończyłeś swoją pierwszą lekcję!",
                        "📚"
                    )
                
                st.success("Lekcja oznaczona jako ukończona!")
                st.rerun()
    
    with col3:
        next_lesson_id = f"b{block_num}_m{module_num}_l{lesson_num+1}"
        if st.button("Następna lekcja →", use_container_width=True):
            st.session_state["lesson_id"] = next_lesson_id
            st.session_state["lesson_title"] = f"Lekcja {lesson_num+1}"
            st.rerun()

def main():
    """
    Main function for the Course Structure page.
    """
    # Ensure pandas is imported
    import pandas as pd
    
    # Setup page
    setup_page(
        page_title=f"Struktura Kursu | {APP_CONFIG['app_name']}",
        page_icon=APP_CONFIG["app_icon"],
        layout="wide"
    )
    
    # Display sidebar navigation
    sidebar_navigation()
    
    # Page header
    page_header(
        title="Struktura Kursu",
        description="Przegląd bloków tematycznych, modułów i lekcji",
        icon="📚"
    )
    
    # If a specific lesson is selected to be shown
    if st.session_state.get("show_lesson", False) and st.session_state.get("lesson_id") and st.session_state.get("lesson_title"):
        display_lesson_content(st.session_state["lesson_id"], st.session_state["lesson_title"])
        
        # Back button
        if st.button("← Wróć do struktury kursu", use_container_width=True):
            st.session_state["show_lesson"] = False
            st.session_state.pop("lesson_id", None)
            st.session_state.pop("lesson_title", None)
            st.rerun()
    else:
        # Show course structure
        display_course_structure()
        
        # Add button to start the first lesson
        st.markdown("### Rozpocznij kurs")
        if st.button("Rozpocznij od pierwszej lekcji", use_container_width=True):
            st.session_state["show_lesson"] = True
            st.session_state["lesson_id"] = "b1_m1_l1"
            st.session_state["lesson_title"] = "Co to jest neuroprzywództwo?"
            st.rerun()

if __name__ == "__main__":
    main()
