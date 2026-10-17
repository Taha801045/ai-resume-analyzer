"""
Launcher for Streamlit Pure-Python UI
Runs: python run_streamlit.py
"""
import sys
from streamlit.web import cli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.headless=false"]
    cli.main()
