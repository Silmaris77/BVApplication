"""
Resources/Blog page for the BrainVenture application.
"""

import streamlit as st
import os
import sys
import json
from datetime import datetime
import random

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.app_config import APP_CONFIG, FEATURE_FLAGS
from components.navigation import sidebar_navigation
from utils.ui import setup_page, card, tag_badge, tabs
from utils.helpers import format_date, load_file, slugify

def main():
    """Main function for the Resources/Blog page."""
    # Setup page configuration
    setup_page(
        page_title=f"Zasoby | {APP_CONFIG['app_name']}",
        page_icon=APP_CONFIG["app_icon"],
        layout="wide",
    )
    
    # Display sidebar navigation
    sidebar_navigation()
    
    # Page header
    st.title("📚 Zasoby i Materiały")
    
    # Create tabs for different content types
    tab_options = ["Artykuły", "Książki", "Badania", "Narzędzia"]
    selected_tab = tabs(tab_options)
    
    # Set up search and filter components
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Wyszukaj", "")
    
    with col2:
        category = st.selectbox(
            "Kategoria",
            ["Wszystkie", "Neurobiologia", "Przywództwo", "Rozwój osobisty", "Zarządzanie zespołem"]
        )
        
    with col3:
        sort_by = st.selectbox(
            "Sortuj według",
            ["Najnowsze", "Najpopularniejsze", "Alfabetycznie"]
        )
    
    # Display content based on selected tab
    if selected_tab == "Artykuły":
        display_articles(search_term, category, sort_by)
    elif selected_tab == "Książki":
        display_books(search_term, category, sort_by)
    elif selected_tab == "Badania":
        display_research(search_term, category, sort_by)
    elif selected_tab == "Narzędzia":
        display_tools(search_term, category, sort_by)

def load_blog_data():
    """
    Load blog/resource data from JSON file or create placeholder data.
    
    In a production app, this would load from a database or CMS.
    
    Returns:
        dict: Blog/resource data.
    """
    # Path to the blog data file
    blog_data_path = os.path.join("data", "content", "blog_resources.json")
    
    # Check if the file exists
    if os.path.exists(blog_data_path):
        try:
            with open(blog_data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            st.error(f"Error loading blog data: {str(e)}")
    
    # If file doesn't exist or has an error, return placeholder data
    return generate_placeholder_blog_data()

def generate_placeholder_blog_data():
    """
    Generate placeholder blog/resource data for demonstration.
    
    Returns:
        dict: Placeholder blog/resource data.
    """
    # Sample article data
    articles = [
        {
            "id": "neurobiologia-stresu",
            "title": "Neurobiologia stresu: jak mózg reaguje na wyzwania",
            "summary": "Poznaj mechanizmy neurobiologiczne związane z reakcją na stres i jak możesz je wykorzystać w przywództwie.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.",
            "image": "brain_stress.jpg",
            "author": "Dr Anna Kowalska",
            "published_date": "2025-05-01",
            "category": "Neurobiologia",
            "tags": ["stres", "mózg", "zarządzanie stresem", "neuroplastyczność"],
            "read_time": 8,
            "views": 1240,
            "featured": True
        },
        {
            "id": "5-technik-zarzadzania-stresem",
            "title": "5 technik zarządzania stresem w oparciu o neurobiologię",
            "summary": "Praktyczne wskazówki jak wykorzystać wiedzę o mózgu do lepszego radzenia sobie ze stresem.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.",
            "image": "stress_management.jpg",
            "author": "Marek Nowak",
            "published_date": "2025-05-15",
            "category": "Przywództwo",
            "tags": ["stres", "techniki", "zarządzanie sobą", "produktywność"],
            "read_time": 5,
            "views": 2350,
            "featured": True
        },
        {
            "id": "neuroleadership-praktyka",
            "title": "Neuroleadership w praktyce: przykłady z firm odnoszących sukcesy",
            "summary": "Case studies firm, które z powodzeniem wdrożyły zasady neuroprzywództwa.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.",
            "image": "leadership_cases.jpg",
            "author": "Katarzyna Wiśniewska",
            "published_date": "2025-04-28",
            "category": "Przywództwo",
            "tags": ["case study", "wdrożenia", "kultura organizacyjna", "praktyka"],
            "read_time": 12,
            "views": 870,
            "featured": False
        },
        {
            "id": "emocje-decyzje-liderow",
            "title": "Jak emocje wpływają na decyzje liderów?",
            "summary": "Poznaj neurobiologiczne podstawy podejmowania decyzji w kontekście emocji.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.",
            "image": "emotions_decisions.jpg",
            "author": "Dr Tomasz Adamski",
            "published_date": "2025-05-10",
            "category": "Neurobiologia",
            "tags": ["emocje", "decyzje", "zarządzanie emocjami", "inteligencja emocjonalna"],
            "read_time": 10,
            "views": 1560,
            "featured": False
        },
        {
            "id": "budowanie-zespolu-neuro",
            "title": "Budowanie zespołu w oparciu o zrozumienie mózgu",
            "summary": "Jak wykorzystać wiedzę o neurobiologii w tworzeniu efektywnych zespołów.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl. Sed euismod, nisl sit amet ultricies lacinia, nisl nisl aliquam nisl, eget aliquam nisl nisl sit amet nisl.",
            "image": "team_building.jpg",
            "author": "Magdalena Jabłońska",
            "published_date": "2025-05-20",
            "category": "Zarządzanie zespołem",
            "tags": ["zespół", "budowanie zespołu", "współpraca", "efektywność"],
            "read_time": 7,
            "views": 980,
            "featured": False
        }
    ]
    
    # Sample book data
    books = [
        {
            "id": "neuroleadership-podstawy",
            "title": "Neuroleadership: Podstawy naukowe nowego przywództwa",
            "author": "Dr David Rock",
            "summary": "Kompletny przewodnik po podstawach neuroprzywództwa oparty na najnowszych badaniach.",
            "cover_image": "book_rock.jpg",
            "published_year": 2023,
            "publisher": "Neuro Press",
            "category": "Przywództwo",
            "tags": ["podstawy", "neurobiologia", "przywództwo"],
            "rating": 4.8,
            "isbn": "978-3-16-148410-0"
        },
        {
            "id": "mozg-lidera",
            "title": "Mózg Lidera: Neurobiologia skutecznego zarządzania",
            "author": "Prof. Maria Kowalczyk",
            "summary": "Jak mózg wpływa na zdolności przywódcze i jak rozwijać struktury mózgowe odpowiedzialne za przywództwo.",
            "cover_image": "book_brain.jpg",
            "published_year": 2024,
            "publisher": "Brain Science Publishing",
            "category": "Neurobiologia",
            "tags": ["mózg", "neurobiologia", "rozwój"],
            "rating": 4.5,
            "isbn": "978-1-56619-909-4"
        },
        {
            "id": "zespol-neurobiologia",
            "title": "Zespół z Perspektywy Neurobiologii",
            "author": "Jan Wiśniewski",
            "summary": "Jak wykorzystać wiedzę o funkcjonowaniu mózgu do tworzenia zgranych i efektywnych zespołów.",
            "cover_image": "book_team.jpg",
            "published_year": 2024,
            "publisher": "Team Science",
            "category": "Zarządzanie zespołem",
            "tags": ["zespół", "współpraca", "neurobiologia"],
            "rating": 4.3,
            "isbn": "978-0-12345-678-9"
        },
    ]
    
    # Sample research data
    research = [
        {
            "id": "stress-leadership-performance",
            "title": "Wpływ stresu na podejmowanie decyzji przez liderów",
            "authors": ["Smith, J.", "Johnson, R.", "Williams, A."],
            "institution": "Uniwersytet Warszawski",
            "summary": "Badanie analizujące neurologiczne mechanizmy wpływu stresu na proces podejmowania decyzji przez osoby na stanowiskach kierowniczych.",
            "published_date": "2025-03-15",
            "category": "Neurobiologia",
            "tags": ["stres", "decyzje", "przywództwo", "badania kliniczne"],
            "doi": "10.1234/neuro.2025.01.002",
            "url": "https://example.org/research/0001"
        },
        {
            "id": "team-dynamics-brain",
            "title": "Dynamika zespołu z perspektywy aktywności mózgu",
            "authors": ["Kowalski, T.", "Nowak, A.", "Jabłoński, P."],
            "institution": "Instytut Badań Neurologicznych",
            "summary": "Nowatorskie badanie wykorzystujące fMRI do analizy aktywności mózgu członków zespołu podczas współpracy.",
            "published_date": "2025-04-10",
            "category": "Zarządzanie zespołem",
            "tags": ["zespół", "fMRI", "współpraca", "neurobiologia"],
            "doi": "10.1234/neuro.2025.03.015",
            "url": "https://example.org/research/0002"
        },
    ]
    
    # Sample tool data
    tools = [
        {
            "id": "neuro-stress-tracker",
            "title": "Neuro Stress Tracker",
            "description": "Aplikacja do monitorowania poziomu stresu w oparciu o biomarkery i oferująca techniki redukcji stresu oparte na neurobiologii.",
            "image": "tool_stress.jpg",
            "category": "Zarządzanie sobą",
            "tags": ["stres", "aplikacja", "monitorowanie", "redukcja"],
            "url": "https://example.com/neuro-stress-tracker",
            "price": "Free / Premium",
            "rating": 4.7
        },
        {
            "id": "decision-master",
            "title": "Decision Master",
            "description": "Narzędzie wspierające podejmowanie decyzji w oparciu o modele neurobiologiczne, pomagające ograniczyć wpływ błędów poznawczych.",
            "image": "tool_decision.jpg",
            "category": "Przywództwo",
            "tags": ["decyzje", "aplikacja", "błędy poznawcze"],
            "url": "https://example.com/decision-master",
            "price": "Subscription",
            "rating": 4.5
        },
        {
            "id": "team-neuro-analyzer",
            "title": "Team Neuro Analyzer",
            "description": "Platforma do analizy dynamiki zespołu i dopasowania ról w oparciu o profile neurobiologiczne członków zespołu.",
            "image": "tool_team.jpg",
            "category": "Zarządzanie zespołem",
            "tags": ["zespół", "analiza", "role", "dopasowanie"],
            "url": "https://example.com/team-neuro-analyzer",
            "price": "Enterprise",
            "rating": 4.6
        },
    ]
    
    return {
        "articles": articles,
        "books": books,
        "research": research,
        "tools": tools
    }

def display_article(article):
    """
    Display a blog article card.
    
    Args:
        article (dict): Article data.
    """
    # Format date
    try:
        date_obj = datetime.strptime(article["published_date"], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d %b %Y")
    except:
        formatted_date = article.get("published_date", "")
    
    # Generate article card
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        # Image column
        with col1:
            # Use a placeholder image if the actual image doesn't exist
            image_path = os.path.join("static", "images", "blog", article.get("image", "placeholder.jpg"))
            if not os.path.exists(image_path):
                st.image("https://via.placeholder.com/300x200?text=BrainVenture", width=200)
            else:
                st.image(image_path, width=200)
        
        # Content column
        with col2:
            # Title with link
            st.markdown(f"### {article['title']}")
            
            # Author and date
            st.markdown(f"**{article.get('author', '')}** • {formatted_date} • {article.get('read_time', 5)} min czytania")
            
            # Summary
            st.markdown(f"{article.get('summary', '')}")
            
            # Tags
            tags_html = ""
            for tag in article.get("tags", [])[:3]:
                tags_html += tag_badge(tag)
            st.markdown(tags_html, unsafe_allow_html=True)
            
            # Read more button
            st.button(f"Czytaj więcej", key=f"read_more_{article['id']}")
        
        st.divider()

def display_articles(search_term="", category="Wszystkie", sort_by="Najnowsze"):
    """
    Display blog articles with filtering and sorting.
    
    Args:
        search_term (str): Search term to filter articles.
        category (str): Category to filter articles.
        sort_by (str): Sorting method.
    """
    # Load blog data
    blog_data = load_blog_data()
    articles = blog_data.get("articles", [])
    
    # Apply filters
    if search_term:
        articles = [a for a in articles if search_term.lower() in a.get("title", "").lower() or 
                    search_term.lower() in a.get("summary", "").lower() or
                    any(search_term.lower() in tag.lower() for tag in a.get("tags", []))]
    
    if category != "Wszystkie":
        articles = [a for a in articles if a.get("category") == category]
    
    # Sort articles
    if sort_by == "Najnowsze":
        articles = sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)
    elif sort_by == "Najpopularniejsze":
        articles = sorted(articles, key=lambda x: x.get("views", 0), reverse=True)
    elif sort_by == "Alfabetycznie":
        articles = sorted(articles, key=lambda x: x.get("title", ""))
    
    # Check if any articles match the filters
    if not articles:
        st.info("Nie znaleziono artykułów spełniających podane kryteria.")
        return
    
    # Featured articles
    featured_articles = [a for a in articles if a.get("featured", False)]
    if featured_articles and not search_term and category == "Wszystkie":
        st.header("Wyróżnione Artykuły")
        
        # Display featured articles in a grid
        cols = st.columns(min(len(featured_articles), 2))
        for i, article in enumerate(featured_articles[:2]):
            with cols[i % 2]:
                # Use a placeholder image if the actual image doesn't exist
                image_path = os.path.join("static", "images", "blog", article.get("image", "placeholder.jpg"))
                if not os.path.exists(image_path):
                    st.image("https://via.placeholder.com/600x300?text=BrainVenture+Featured", use_column_width=True)
                else:
                    st.image(image_path, use_column_width=True)
                
                st.markdown(f"### {article['title']}")
                st.markdown(f"{article.get('summary', '')}")
                st.button(f"Czytaj więcej", key=f"featured_{article['id']}")
        
        st.divider()
        st.header("Wszystkie Artykuły")
    
    # Display all matching articles
    for article in articles:
        display_article(article)

def display_books(search_term="", category="Wszystkie", sort_by="Najnowsze"):
    """
    Display books with filtering and sorting.
    
    Args:
        search_term (str): Search term to filter books.
        category (str): Category to filter books.
        sort_by (str): Sorting method.
    """
    # Load blog data
    blog_data = load_blog_data()
    books = blog_data.get("books", [])
    
    # Apply filters
    if search_term:
        books = [b for b in books if search_term.lower() in b.get("title", "").lower() or 
                search_term.lower() in b.get("author", "").lower() or 
                search_term.lower() in b.get("summary", "").lower() or
                any(search_term.lower() in tag.lower() for tag in b.get("tags", []))]
    
    if category != "Wszystkie":
        books = [b for b in books if b.get("category") == category]
    
    # Sort books
    if sort_by == "Najnowsze":
        books = sorted(books, key=lambda x: x.get("published_year", 0), reverse=True)
    elif sort_by == "Najpopularniejsze":
        books = sorted(books, key=lambda x: x.get("rating", 0), reverse=True)
    elif sort_by == "Alfabetycznie":
        books = sorted(books, key=lambda x: x.get("title", ""))
    
    # Check if any books match the filters
    if not books:
        st.info("Nie znaleziono książek spełniających podane kryteria.")
        return
    
    # Display books in a grid
    book_cols = st.columns(3)
    for i, book in enumerate(books):
        with book_cols[i % 3]:
            # Use a placeholder image if the actual image doesn't exist
            image_path = os.path.join("static", "images", "books", book.get("cover_image", "placeholder.jpg"))
            if not os.path.exists(image_path):
                st.image("https://via.placeholder.com/200x300?text=Book+Cover", width=150)
            else:
                st.image(image_path, width=150)
            
            st.markdown(f"### {book['title']}")
            st.markdown(f"**Autor:** {book.get('author', '')}")
            st.markdown(f"**Rok:** {book.get('published_year', '')}")
            st.markdown(f"**Ocena:** {'⭐' * round(book.get('rating', 0))}")
            st.button(f"Szczegóły", key=f"book_{book['id']}")

def display_research(search_term="", category="Wszystkie", sort_by="Najnowsze"):
    """
    Display research papers with filtering and sorting.
    
    Args:
        search_term (str): Search term to filter research.
        category (str): Category to filter research.
        sort_by (str): Sorting method.
    """
    # Load blog data
    blog_data = load_blog_data()
    research_papers = blog_data.get("research", [])
    
    # Apply filters
    if search_term:
        research_papers = [r for r in research_papers if search_term.lower() in r.get("title", "").lower() or 
                          search_term.lower() in " ".join(r.get("authors", [])).lower() or
                          search_term.lower() in r.get("summary", "").lower() or
                          any(search_term.lower() in tag.lower() for tag in r.get("tags", []))]
    
    if category != "Wszystkie":
        research_papers = [r for r in research_papers if r.get("category") == category]
    
    # Sort research
    if sort_by == "Najnowsze":
        research_papers = sorted(research_papers, key=lambda x: x.get("published_date", ""), reverse=True)
    elif sort_by == "Najpopularniejsze":
        # For research, we don't have views, so we sort by recency as fallback
        research_papers = sorted(research_papers, key=lambda x: x.get("published_date", ""), reverse=True)
    elif sort_by == "Alfabetycznie":
        research_papers = sorted(research_papers, key=lambda x: x.get("title", ""))
    
    # Check if any research papers match the filters
    if not research_papers:
        st.info("Nie znaleziono badań spełniających podane kryteria.")
        return
    
    # Display research papers
    for paper in research_papers:
        with st.container():
            st.markdown(f"### {paper['title']}")
            st.markdown(f"**Autorzy:** {', '.join(paper.get('authors', []))}")
            st.markdown(f"**Instytucja:** {paper.get('institution', '')}")
            st.markdown(f"**Opublikowano:** {paper.get('published_date', '')}")
            st.markdown(f"**DOI:** {paper.get('doi', 'N/A')}")
            
            st.markdown(f"{paper.get('summary', '')}")
            
            # Tags
            tags_html = ""
            for tag in paper.get("tags", [])[:3]:
                tags_html += tag_badge(tag)
            st.markdown(tags_html, unsafe_allow_html=True)
            
            # URL button
            st.button(f"Czytaj badanie", key=f"research_{paper['id']}")
            
            st.divider()

def display_tools(search_term="", category="Wszystkie", sort_by="Najnowsze"):
    """
    Display tools with filtering and sorting.
    
    Args:
        search_term (str): Search term to filter tools.
        category (str): Category to filter tools.
        sort_by (str): Sorting method.
    """
    # Load blog data
    blog_data = load_blog_data()
    tools = blog_data.get("tools", [])
    
    # Apply filters
    if search_term:
        tools = [t for t in tools if search_term.lower() in t.get("title", "").lower() or 
                search_term.lower() in t.get("description", "").lower() or
                any(search_term.lower() in tag.lower() for tag in t.get("tags", []))]
    
    if category != "Wszystkie":
        tools = [t for t in tools if t.get("category") == category]
    
    # Sort tools
    if sort_by == "Najnowsze":
        # For tools, we don't have a date, so we sort by rating as fallback
        tools = sorted(tools, key=lambda x: x.get("rating", 0), reverse=True)
    elif sort_by == "Najpopularniejsze":
        tools = sorted(tools, key=lambda x: x.get("rating", 0), reverse=True)
    elif sort_by == "Alfabetycznie":
        tools = sorted(tools, key=lambda x: x.get("title", ""))
    
    # Check if any tools match the filters
    if not tools:
        st.info("Nie znaleziono narzędzi spełniających podane kryteria.")
        return
    
    # Display tools in a grid
    tool_cols = st.columns(2)
    for i, tool in enumerate(tools):
        with tool_cols[i % 2]:
            with st.container():
                col1, col2 = st.columns([1, 2])
                
                # Image column
                with col1:
                    # Use a placeholder image if the actual image doesn't exist
                    image_path = os.path.join("static", "images", "tools", tool.get("image", "placeholder.jpg"))
                    if not os.path.exists(image_path):
                        st.image("https://via.placeholder.com/200x200?text=Tool", width=150)
                    else:
                        st.image(image_path, width=150)
                
                # Content column
                with col2:
                    st.markdown(f"### {tool['title']}")
                    st.markdown(f"**Kategoria:** {tool.get('category', '')}")
                    st.markdown(f"**Ocena:** {'⭐' * round(tool.get('rating', 0))}")
                    st.markdown(f"**Cena:** {tool.get('price', 'N/A')}")
                    
                st.markdown(f"{tool.get('description', '')}")
                
                # Tags
                tags_html = ""
                for tag in tool.get("tags", [])[:3]:
                    tags_html += tag_badge(tag)
                st.markdown(tags_html, unsafe_allow_html=True)
                
                # URL button
                st.button(f"Sprawdź narzędzie", key=f"tool_{tool['id']}")
                
            st.divider()

if __name__ == "__main__":
    main()
