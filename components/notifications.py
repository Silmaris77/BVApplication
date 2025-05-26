"""
Notification components for the BrainVenture application.
"""

import streamlit as st
import time
from datetime import datetime

def show_toast(title, message, icon="ℹ️"):
    """
    Show a toast notification using Streamlit's toast API.
    
    Args:
        title (str): Toast notification title.
        message (str): Toast notification message.
        icon (str): Toast notification icon (emoji).
    """
    st.toast(f"{icon} {message}", icon=icon)

def show_success_notification(message):
    """
    Show a success notification.
    
    Args:
        message (str): Success message.
    """
    show_toast("Sukces", message, icon="✅")

def show_error_notification(message):
    """
    Show an error notification.
    
    Args:
        message (str): Error message.
    """
    show_toast("Błąd", message, icon="❌")

def show_info_notification(message):
    """
    Show an info notification.
    
    Args:
        message (str): Info message.
    """
    show_toast("Informacja", message, icon="ℹ️")

def show_warning_notification(message):
    """
    Show a warning notification.
    
    Args:
        message (str): Warning message.
    """
    show_toast("Ostrzeżenie", message, icon="⚠️")

def show_achievement_notification(achievement_name):
    """
    Show a notification when user earns an achievement.
    
    Args:
        achievement_name (str): Achievement name.
    """
    show_toast(
        "Nowe osiągnięcie!",
        f"Zdobyłeś osiągnięcie: {achievement_name}",
        icon="🏆"
    )

def show_notifications_center():
    """
    Display the notifications center in the sidebar.
    """
    with st.sidebar.expander("📬 Powiadomienia", expanded=False):
        notifications = get_user_notifications()
        
        if not notifications:
            st.markdown("Brak nowych powiadomień.")
        else:
            for notification in notifications:
                notification_type = notification.get("type", "info")
                icon_map = {
                    "success": "✅",
                    "error": "❌",
                    "warning": "⚠️",
                    "achievement": "🏆",
                    "info": "ℹ️"
                }
                icon = icon_map.get(notification_type, "ℹ️")
                
                # Display notification
                with st.container():
                    st.markdown(f"### {icon} {notification.get('title', 'Powiadomienie')}")
                    st.markdown(notification.get("message", ""))
                    st.markdown(f"*{notification.get('time', 'Teraz')}*")
                    
                    # Mark as read button
                    if st.button("Oznacz jako przeczytane", key=f"notif_{notification.get('id')}"):
                        # In a real app, this would update the notification status in the database
                        st.success("Powiadomienie oznaczone jako przeczytane.")
                    
                    st.divider()

def get_user_notifications():
    """
    Get user notifications.
    
    Returns:
        list: List of notification objects.
    """
    # In a real app, this would fetch notifications from a database
    # For the MVP, we'll return a static list for demonstration
    if "notifications" not in st.session_state:
        st.session_state["notifications"] = [
            {
                "id": "notif_1",
                "type": "info",
                "title": "Witaj w kursie!",
                "message": "Rozpocznij naukę neuroprzywództwa już teraz.",
                "time": "Przed chwilą",
                "read": False
            },
            {
                "id": "notif_2",
                "type": "achievement",
                "title": "Nowe osiągnięcie!",
                "message": "Zdobyłeś osiągnięcie: Pierwszy krok",
                "time": "Wczoraj",
                "read": False
            }
        ]
    
    return st.session_state["notifications"]

def create_notification(notification_type, title, message):
    """
    Create a new notification.
    
    Args:
        notification_type (str): Notification type ('info', 'success', 'error', 'warning', 'achievement').
        title (str): Notification title.
        message (str): Notification message.
    """
    # In a real app, this would save the notification to a database
    # For the MVP, we'll add it to the session state
    if "notifications" not in st.session_state:
        st.session_state["notifications"] = []
    
    notification_id = f"notif_{int(time.time())}"
    now = datetime.now()
    
    # Create notification object
    notification = {
        "id": notification_id,
        "type": notification_type,
        "title": title,
        "message": message,
        "time": "Teraz",  # In a real app, format the datetime
        "read": False
    }
    
    # Add to notifications list
    st.session_state["notifications"].insert(0, notification)  # Add at the beginning
    
    # Show a toast notification
    show_toast(title, message)
