"""
Neuroleader Types page for the BrainVenture application.
"""

import streamlit as st
import os
import sys
import json
import random
from datetime import datetime

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.app_config import APP_CONFIG
from config.content_config import load_neuroleader_types, load_neuroleader_test, get_neuroleader_type_details
from components.navigation import sidebar_navigation, page_header
from utils.ui import setup_page, card
from utils.helpers import load_user_data, save_user_data, award_achievement
from utils.validators import validate_test_answers

def display_neuroleader_type(type_id):
    """
    Display detailed information about a neuroleader type.
    
    Args:
        type_id (str): ID of the neuroleader type to display.
    """
    # Get type details including markdown content
    type_details = get_neuroleader_type_details(type_id)
    
    if not type_details:
        st.error(f"Nie znaleziono informacji o typie: {type_id}")
        return
    
    # If markdown content is available, display it
    if "markdown_content" in type_details:
        st.markdown(type_details["markdown_content"])
    else:
        # Fallback to basic display if markdown is not available
        st.markdown(f"# {type_details.get('icon', '🧠')} {type_details.get('name', 'Typ Neurolidera')}")
        
        st.markdown("## Charakterystyka")
        st.markdown(type_details.get("short_description", ""))
        
        st.markdown("## Supermoc")
        st.markdown(type_details.get("supermoc", ""))
        
        st.markdown("## Słabość")
        st.markdown(type_details.get("slabość", ""))
        
        st.markdown("## Neurobiologia")
        st.markdown(type_details.get("neurobiologia", ""))

def display_neuroleader_types_overview():
    """
    Display an overview of all neuroleader types.
    """
    st.markdown("# Typy Neuroleaderów")
    st.markdown("""
    Każdy lider ma swój unikalny styl przywództwa, który jest kształtowany przez procesy neurobiologiczne zachodzące w jego mózgu.
    Poznaj sześć typów Neuroleaderów i odkryj, który z nich najlepiej opisuje Twój styl przywództwa.
    """)
    
    # Load all neuroleader types
    neuroleader_types = load_neuroleader_types()
    
    # Display types in a grid
    cols = st.columns(3)
    for i, ntype in enumerate(neuroleader_types):
        with cols[i % 3]:
            type_icon = ntype.get("icon", "🧠")
            type_name = ntype.get("name", "Typ Neurolidera")
            type_desc = ntype.get("short_description", "")
            
            st.markdown(f"### {type_icon} {type_name}")
            st.markdown(type_desc[:100] + "..." if len(type_desc) > 100 else type_desc)
            
            if st.button(f"Dowiedz się więcej", key=f"type_{ntype.get('id', '')}", use_container_width=True):
                st.session_state["selected_type"] = ntype.get("id", "")
                st.session_state["show_type_details"] = True
                st.session_state["show_test"] = False
                st.rerun()


def load_test_questions():
    """
    Load questions for the neuroleader test.
    
    Returns:
        list: A list of question dictionaries.
    """
    test_data = load_neuroleader_test()
    
    # Check if we have valid test data
    if not test_data or "questions" not in test_data:
        return []
        
    # Return the questions list
    return test_data.get("questions", [])


def run_neuroleader_test():
    """
    Run the neuroleader type test with all questions shown at once.
    """
    st.markdown("# Test Typologii Neuroleaderów")
    st.markdown("""
    Ten test pomoże Ci określić Twój dominujący typ neuroliderski.
    Odpowiedz na poniższe pytania, aby uzyskać wgląd w charakterystykę Twojego stylu przywództwa z perspektywy neurobiologicznej.
    """)
    
    # Load test questions
    questions = load_test_questions()
    
    # Make sure we have questions before trying to access them
    if not questions or len(questions) == 0:
        st.error("Nie znaleziono pytań do testu.")
        return
    
    # Initialize answers in session state if not present
    if 'test_answers' not in st.session_state:
        st.session_state.test_answers = {}
    
    # Create a form for all questions at once
    with st.form(key="neuroleader_test_form"):
        for i, question in enumerate(questions):
            st.markdown(f"### Pytanie {i+1}: {question['text']}")
            
            # Create unique key for each question
            question_key = f"question_{i}"
            
            # Radio buttons for answers (1-5 scale)
            answer = st.radio(
                "Wybierz odpowiedź:",
                options=["1", "2", "3", "4", "5"],
                index=int(st.session_state.test_answers.get(question_key, {}).get("value", 0)) - 1 if question_key in st.session_state.test_answers else 0,
                horizontal=True,
                key=question_key
            )
            
            # Store answer in session state
            question_type = question.get("type", "")
            st.session_state.test_answers[question_key] = {
                "value": int(answer),
                "type": question_type
            }
            
            # Add some spacing between questions
            st.write("")
            st.write("---")
        
        # Submit button for the entire form
        submitted = st.form_submit_button("Zakończ test i sprawdź wyniki", use_container_width=True)
    
    if submitted:
        # Validate answers
        valid, completion_percentage, message = validate_test_answers(
            st.session_state.test_answers,
            len(questions)
        )
        
        if valid:
            # Process answers and determine the type
            result_type = process_test_results(st.session_state.test_answers)
            
            # Save result to user data
            user_id = "default_user"  # In a real app, this would come from authentication
            user_data = load_user_data(user_id)
            
            if "progress" not in user_data:
                user_data["progress"] = {}
            
            user_data["progress"]["neuroleader_type"] = result_type
            user_data["progress"]["tests_taken"] = user_data["progress"].get("tests_taken", []) + [{
                "test_type": "neuroleader_type",
                "result": result_type,
                "date": datetime.now().strftime("%d-%m-%Y")
            }]
            
            save_user_data(user_data, user_id)
            
            # Award achievement
            award_achievement(
                user_id,
                "Samoświadomy Lider",
                "Wykonałeś swój pierwszy test neuroleaderski i poznałeś swój typ!",
                "🔍"
            )
            
            # Show result
            st.session_state["test_result"] = result_type
            st.session_state["show_test_result"] = True
            st.session_state["show_test"] = False
            st.rerun()
        else:
            st.warning(message)

def process_test_results(answers):
    """
    Process test answers and determine the dominant neuroleader type.
    
    Args:
        answers (dict): User answers from the test.
        
    Returns:
        str: Dominant neuroleader type ID.
    """
    # In a more sophisticated implementation, this would use proper scoring
    # For the MVP, we'll count the frequency of each type in the answers
    type_scores = {
        "neuroanalityk": 0,
        "neuroreaktor": 0,
        "neurobalanser": 0,
        "neuroempata": 0,
        "neuroinnowator": 0,
        "neuroinspirator": 0
    }
    
    for question_id, answer_data in answers.items():
        answer_type = answer_data.get("type", "")
        answer_value = answer_data.get("value", 0)
        
        if answer_type in type_scores:
            type_scores[answer_type] += answer_value
    
    # Find the type with the highest score
    dominant_type = max(type_scores, key=lambda t: type_scores[t])
    
    # If there's a tie, break it randomly
    max_score = type_scores[dominant_type]
    tied_types = [t for t, s in type_scores.items() if s == max_score]
    
    if len(tied_types) > 1:
        dominant_type = random.choice(tied_types)
    
    return dominant_type

def show_test_result(result_type):
    """
    Show the results of the neuroleader type test.
    
    Args:
        result_type (str): Dominant neuroleader type ID.
    """
    st.markdown("# Twój Wynik Testu")
    
    # Get type details
    type_details = get_neuroleader_type_details(result_type)
    
    if not type_details:
        st.error(f"Nie znaleziono informacji o typie: {result_type}")
        return
    
    # Display result
    st.markdown(f"""
    ## Twój dominujący typ to:
    # {type_details.get('icon', '🧠')} {type_details.get('name', 'Typ Neurolidera')}
    """)
    
    st.markdown("### Charakterystyka")
    st.markdown(type_details.get("short_description", ""))
    
    # Display superpowers and weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Twoja supermoc")
        st.markdown(type_details.get("supermoc", ""))
    
    with col2:
        st.markdown("### Twoja słabość")
        st.markdown(type_details.get("slabość", ""))
    
    # Show learn more button
    if st.button("Zobacz pełną charakterystykę", use_container_width=True):
        st.session_state["selected_type"] = result_type
        st.session_state["show_type_details"] = True
        st.session_state["show_test_result"] = False
        st.rerun()
    
    # Option to retake the test
    if st.button("Wykonaj test ponownie", use_container_width=True):
        st.session_state["show_test"] = True
        st.session_state["show_test_result"] = False
        st.session_state["test_answers"] = {}
        st.rerun()

def main():
    """
    Main function for the Neuroleader Types page.
    """
    # Setup page
    setup_page(
        page_title=f"Typy Neuroleaderów | {APP_CONFIG['app_name']}",
        page_icon=APP_CONFIG["app_icon"],
        layout="wide"
    )
    
    # Display sidebar navigation
    sidebar_navigation()
    
    # Page header
    page_header(
        title="Typy Neuroleaderów",
        description="Poznaj style przywództwa oparte na neurobiologii",
        icon="🧩"
    )
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["Typy Neuroleaderów", "Test Typologii"])
    
    with tab1:
        # If a specific type is selected to be shown
        if st.session_state.get("show_type_details", False) and st.session_state.get("selected_type"):
            display_neuroleader_type(st.session_state["selected_type"])
            
            # Back button
            if st.button("← Wróć do przeglądu typów", use_container_width=True):
                st.session_state["show_type_details"] = False
                st.session_state.pop("selected_type", None)
                st.rerun()
        else:
            # Show overview of all types
            display_neuroleader_types_overview()
    
    with tab2:
        # If test result should be shown
        if st.session_state.get("show_test_result", False) and st.session_state.get("test_result"):
            show_test_result(st.session_state["test_result"])
        # If test should be shown
        elif st.session_state.get("show_test", False):
            run_neuroleader_test()
        else:
            # Show test introduction
            st.markdown("# Test Typologii Neuroleaderów")
            st.markdown("""
            Poznaj swój dominujący styl przywództwa z perspektywy neurobiologicznej!
            
            Ten test składa się z 18 pytań, które pomogą Ci odkryć, jakim typem neurolidera jesteś.
            Na podstawie Twoich odpowiedzi, określimy, czy jesteś Neuroempatą, Neuroinnowatorem, 
            Neuroreaktorem, Neuroinspiatorem, Neuroanalitykiem czy może Neurobalanserem.
            """)
            
            # Display sample questions
            st.markdown("### Przykładowe pytania:")
            st.markdown("""
            1. Przed podjęciem decyzji staram się zgromadzić wszystkie możliwe informacje i dane
            2. W sytuacjach stresowych często podejmuję szybkie decyzje, kierując się przede wszystkim instynktem
            3. Potrafię łączyć analizę danych z intuicyjnym wyczuciem sytuacji
            """)
            
            # Start test button
            if st.button("Rozpocznij test", use_container_width=True):
                st.session_state["show_test"] = True
                st.session_state["test_answers"] = {}
                st.rerun()

if __name__ == "__main__":
    main()
