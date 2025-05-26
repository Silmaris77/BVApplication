"""
Neuroleader Types page for the BrainVenture application.
"""

import streamlit as st
import os
import sys
import json
import random
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

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
    Display detailed information about a neuroleader type with modern styling.
    
    Args:
        type_id (str): ID of the neuroleader type to display.
    """    # Get type details including markdown content
    type_details = get_neuroleader_type_details(type_id)
    
    if not type_details:
        st.error(f"Nie znaleziono informacji o typie: {type_id}")
        return
    
    # Styles are now loaded from external CSS file
    
    # Header with type name and icon
    st.markdown(f"""
    <div class="type-header">
        <span class="type-icon">{type_details.get('icon', '🧠')}</span>
        <h1 class="type-name">{type_details.get('name', 'Typ Neurolidera')}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # If markdown content is available, display it
    if "markdown_content" in type_details:
        with st.container():
            st.markdown('<div class="info-section">', unsafe_allow_html=True)
            st.markdown(type_details["markdown_content"])
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Fallback to beautiful card layout if markdown is not available
        with st.container():
            st.markdown('<div class="info-section">', unsafe_allow_html=True)
            
            # Charakterystyka
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #4CAF50;">
                <h2>Charakterystyka</h2>
                {type_details.get("short_description", "")}
            </div>
            """, unsafe_allow_html=True)
            
            # Supermoc
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #2196F3;">
                <h2>Supermoc</h2>
                {type_details.get("supermoc", "")}
            </div>
            """, unsafe_allow_html=True)
            
            # Słabość
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #FF9800;">
                <h2>Słabość</h2>
                {type_details.get("slabość", "")}
            </div>
            """, unsafe_allow_html=True)
            
            # Neurobiologia
            st.markdown(f"""
            <div class="info-card" style="border-left-color: #9C27B0;">
                <h2>Neurobiologia</h2>
                {type_details.get("neurobiologia", "")}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Add recommendations section
    st.markdown("""
    <div class="info-section" style="margin-top: 1.5rem;">
        <h2>Rozwój i rekomendacje</h2>
        <p>Bazując na Twoim typie neuroleaderskim, polecamy:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommendation cards in a grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; height: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <h3 style="color: #4CAF50;">📚 Materiały do nauki</h3>
            <p>Spersonalizowane zasoby, które pomogą Ci wzmocnić swoje mocne strony i pracować nad wyzwaniami.</p>
            <button style="background: #4CAF50; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; width: 100%;">
                Zobacz zasoby
            </button>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; height: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <h3 style="color: #2196F3;">🔄 Plan rozwoju</h3>
            <p>Spersonalizowany plan rozwoju Twoich kompetencji przywódczych dostosowany do Twojego typu.</p>
            <button style="background: #2196F3; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; width: 100%;">
                Stwórz plan
            </button>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 10px; height: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <h3 style="color: #FF9800;">👥 Znajdź mentora</h3>
            <p>Połącz się z doświadczonymi liderami, którzy reprezentują ten sam typ neuroleaderski.</p>
            <button style="background: #FF9800; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; width: 100%;">
                Znajdź mentora
            </button>
        </div>
        """, unsafe_allow_html=True)
    

def display_neuroleader_types_overview():
    """
    Display an overview of all neuroleader types with modern Material Design cards.
    """
    st.markdown("""
    <h1 style="text-align: center;">Typy Neuroleaderów</h1>
    <p style="text-align: center; max-width: 800px; margin: 0 auto; margin-bottom: 2rem;">
        Każdy lider ma swój unikalny styl przywództwa, który jest kształtowany przez procesy neurobiologiczne 
        zachodzące w jego mózgu. Poznaj sześć typów Neuroleaderów i odkryj, który z nich najlepiej opisuje 
        Twój styl przywództwa.
    </p>
    """, unsafe_allow_html=True)
    
    # Load all neuroleader types
    neuroleader_types = load_neuroleader_types()
      # Styles are now loaded from external CSS file
      # Create a grid layout with streamlit columns instead of CSS grid for better control
    rows = [st.columns(3) for _ in range((len(neuroleader_types) + 2) // 3)]
    
    # Display types in a grid using Streamlit's column layout
    for i, ntype in enumerate(neuroleader_types):
        row_idx = i // 3
        col_idx = i % 3
        
        with rows[row_idx][col_idx]:
            type_icon = ntype.get("icon", "🧠")
            type_name = ntype.get("name", "Typ Neurolidera")
            type_desc = ntype.get("short_description", "")
            type_id = ntype.get("id", "")
            
            # Create color variations for each card
            colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#E91E63", "#3F51B5"]
            card_color = colors[i % len(colors)]
            
            # Create card for each type with enhanced styling
            st.markdown(f"""
            <div class="neuro-card" style="border-top-color: {card_color}; height: auto;">
                <div class="neuro-icon">{type_icon}</div>
                <h3 class="neuro-title" style="color: {card_color};">{type_name}</h3>
                <p class="neuro-desc">{type_desc[:150] + "..." if len(type_desc) > 150 else type_desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add button directly below each card
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
    """    # Modern header styling
    st.markdown("""
    <div class="test-header">
        <h1>Test Typologii Neuroleaderów</h1>
        <p>
            Ten test pomoże Ci określić Twój dominujący typ neuroliderski.
            Odpowiedz na poniższe pytania, aby uzyskać wgląd w charakterystykę Twojego stylu przywództwa z perspektywy neurobiologicznej.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Styles are now loaded from external CSS file
    
    # Load test questions
    questions = load_test_questions()
    
    # Make sure we have questions before trying to access them
    if not questions or len(questions) == 0:
        st.error("Nie znaleziono pytań do testu.")
        return
    
    # Initialize answers in session state if not present
    if 'test_answers' not in st.session_state:
        st.session_state.test_answers = {}
    
    # Create modern progress indicator with percentage
    total_questions = len(questions)
    answered_questions = sum(1 for q in st.session_state.test_answers.values() if q.get("value", 0) > 0)
    completion_percentage = answered_questions / total_questions
    
    st.markdown(f"""
    <div style="margin: 1.5rem 0;">
        <p style="color: #555; font-size: 0.9rem; margin-bottom: 0.5rem;">
            Postęp wypełniania testu: {int(completion_percentage * 100)}%
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(completion_percentage)
    
    # Group questions by type for better organization
    grouped_questions = {}
    for i, question in enumerate(questions):
        q_type = question.get("type", "Inne")
        if q_type not in grouped_questions:
            grouped_questions[q_type] = []
        grouped_questions[q_type].append((i, question))
    
    # Create a form for all questions at once
    with st.form(key="neuroleader_test_form"):
        # Display questions by type with styled cards
        for q_type, q_group in grouped_questions.items():
            st.markdown(f"""
            <div class="section-header">
                {q_type.capitalize()} - pytania
            </div>
            """, unsafe_allow_html=True)
            
            for i, question in q_group:
                # Create styled card for each question with modern design
                with st.container():
                    st.markdown(f"""
                    <div class="question-card">
                        <div class="question-header">
                            <span class="question-number">{i+1}</span>
                            {question['text']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create unique key for each question
                    question_key = f"question_{i}"
                    
                    # Add descriptions for the scale
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        # Radio buttons for answers (1-5 scale) - proper form element with styled labels
                        response = st.radio(
                            "Oceń w skali od 1 do 5:",
                            ["1 - Zdecydowanie nie", "2 - Raczej nie", "3 - Czasami", "4 - Raczej tak", "5 - Zdecydowanie tak"],
                            horizontal=True,
                            key=f"radio_{question_key}",
                            index=int(st.session_state.test_answers.get(question_key, {}).get("value", 0))-1 if st.session_state.test_answers.get(question_key, {}).get("value", 0) > 0 else 2
                        )
                        
                        # Extract numeric value from the response
                        value = int(response[0])
                        
                        # Store this value for form processing later
                        st.session_state.test_answers[question_key] = {
                            "value": value,
                            "type": question.get("type", "")
                        }
          # Submit button for the entire form
        submit_button = st.form_submit_button("Zakończ test i sprawdź wyniki", 
                                use_container_width=True, 
                                type="primary")
    
    # Process form submission outside the form
    if submit_button:
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
    Show the results of the neuroleader type test with modern styling.
    
    Args:
        result_type (str): Dominant neuroleader type ID.
    """
    # Get type details
    type_details = get_neuroleader_type_details(result_type)
    
    if not type_details:
        st.error(f"Nie znaleziono informacji o typie: {result_type}")
        return
    
    # Add confetti animation for celebration
    st.balloons()
      # Header with animation
    st.markdown("""
    <div class="result-header">
        <h1>Twój Wynik Testu</h1>
    </div>
    """, unsafe_allow_html=True)
      # Display result in a beautifully styled card
    st.markdown(f"""
    <div class="result-card">
        <span class="type-icon">{type_details.get('icon', '🧠')}</span>
        <div class="type-name">{type_details.get('name', 'Typ Neurolidera')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display type summary
    st.markdown(f"""
    <div class="result-description">
        <h3>Charakterystyka</h3>
        <p>{type_details.get("short_description", "")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display superpowers and weaknesses with modern cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="superpower-card">
            <h3>🚀 Twoja supermoc</h3>
        """, unsafe_allow_html=True)
        st.markdown(type_details.get("supermoc", ""))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="weakness-card">
            <h3>🛡️ Twoje wyzwanie</h3>
        """, unsafe_allow_html=True)
        st.markdown(type_details.get("slabość", ""))
        st.markdown("</div>", unsafe_allow_html=True)
      # Show comparative chart with other types
    st.markdown("""
    <div class="chart-section">
        <h3>Jak wypadasz na tle innych typów</h3>
    </div>
    """, unsafe_allow_html=True)
      # Create sample data for radar chart
    import pandas as pd
    
    # Create fake scores for demonstration
    categories = ['Analityczność', 'Reaktywność', 'Balans', 'Empatia', 'Innowacyjność', 'Inspirowanie']
    
    # Generate random values but ensure the user's type has highest score
    values = np.random.randint(30, 70, size=6)
    
    # Find index of user's type and ensure it's the highest
    type_indices = {
        "neuroanalityk": 0,
        "neuroreaktor": 1,
        "neurobalanser": 2,
        "neuroempata": 3,
        "neuroinnowator": 4,
        "neuroinspirator": 5
    }
    
    dominant_idx = type_indices.get(result_type, 0)
    values[dominant_idx] = max(values) + 20  # Ensure it's clearly dominant
    
    # Create a radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Twój profil',
        line_color='#4CAF50',
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
      # Action buttons at the bottom
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Zobacz pełną charakterystykę", use_container_width=True, type="primary"):
            st.session_state["selected_type"] = result_type
            st.session_state["show_type_details"] = True
            st.session_state["show_test_result"] = False
            st.rerun()
    
    with col2:
        if st.button("Wykonaj test ponownie", use_container_width=True):
            st.session_state["show_test"] = True
            st.session_state["show_test_result"] = False
            st.session_state["test_answers"] = {}
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add share buttons
    st.markdown("""
    <div class="share-buttons">
        <p>Podziel się swoim wynikiem:</p>
        <div class="social-buttons">
            <button class="facebook-btn">
                <span>Facebook</span>
            </button>
            <button class="twitter-btn">
                <span>Twitter</span>
            </button>
            <button class="linkedin-btn">
                <span>LinkedIn</span>
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
