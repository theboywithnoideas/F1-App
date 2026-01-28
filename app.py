import streamlit as st
import fastf1
import datetime
import pandas as pd
from src.f1_data import get_race_telemetry, load_session # Keeping your logic

# --- Page Config & Styling ---
st.set_page_config(page_title="F1 Arcade Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-baseweb="select"] > div { background-color: #1a1c24; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: Selection Menus ---
st.sidebar.title("🏎️ Race Control")

# 1. Select Year
current_year = datetime.datetime.now().year
year = st.sidebar.selectbox("Select Year", list(range(current_year, 2018, -1)))

# 2. Select Round (Dynamic based on year)
# In a real app, you'd fetch the schedule; here's a simplified version
round_num = st.sidebar.slider("Round Number", 1, 24, 1)

# 3. Select Session
session_type = st.sidebar.selectbox("Session", ["Race", "Qualifying", "Sprint", "Live"])

# 4. "Live" Mode Toggle
if session_type == "Live":
    st.sidebar.warning("Live mode tracks current weekend telemetry.")
    auto_refresh = st.sidebar.checkbox("Auto-refresh (every 30s)", value=True)

# --- Main Logic ---
st.title(f"F1 {year} - Round {round_num} Replay")

@st.cache_data
def get_cached_session(y, r, s):
    # Map friendly names to FastF1 codes
    mapping = {"Race": "R", "Qualifying": "Q", "Sprint": "S"}
    code = mapping.get(s, "R")
    try:
        session = fastf1.get_session(y, r, code)
        session.load()
        return session
    except:
        return None

if st.button("🚀 Load Session"):
    with st.spinner("Fetching Telemetry Data..."):
        session = get_cached_session(year, round_num, session_type)
        
        if session:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("Track Layout & Telemetry")
                # Here you would call your 'run_arcade_replay' but 
                # instead of a popup window, we'd render it as a Plotly chart
                st.info("Visualizing track map with neon overlays...")
                # [Placeholder for your Track Map logic]
                
            with col2:
                st.subheader("Leaderboard")
                results = session.results[['Abbreviation', 'TeamName', 'Position']]
                st.table(results.set_index('Position'))
        else:
            st.error("Session data not available yet!")
