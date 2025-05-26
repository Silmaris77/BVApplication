"""
BrainVenture Application Launcher Script
"""

import os
import sys
import subprocess
import webbrowser

def main():
    """
    Main function to launch the BrainVenture application.
    Installs requirements if needed and launches the Streamlit app.
    """
    print("=" * 60)
    print("Launching BrainVenture: Kurs Neuroprzywództwa")
    print("=" * 60)

    # Check if requirements are installed
    try:
        import streamlit
        print("✅ Streamlit is already installed")
    except ImportError:
        print("⚙️ Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements. Please run 'pip install -r requirements.txt' manually.")
            return

    # Get the absolute path to app.py
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    
    # Check if app.py exists
    if not os.path.exists(app_path):
        print(f"❌ Could not find app.py at {app_path}")
        return
    
    # Launch the application
    print("🚀 Launching BrainVenture application...")
    port = 8501  # Default Streamlit port
    
    # Try to open the browser automatically
    try:
        webbrowser.open(f"http://localhost:{port}")
        print(f"📱 Opening browser to http://localhost:{port}")
    except:
        print(f"ℹ️ Please open your browser to http://localhost:{port}")
    
    # Run Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except KeyboardInterrupt:
        print("\n👋 BrainVenture application stopped.")
    except Exception as e:
        print(f"❌ Error running the application: {e}")
        print("Please run 'streamlit run app.py' manually.")

if __name__ == "__main__":
    main()
