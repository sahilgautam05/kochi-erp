import streamlit as st
import streamlit.components.v1 as components
import os
import sys

st.set_page_config(
    page_title="Kochi Metro Rail Limited (KMRL)",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit UI elements for seamless full-page web app display
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar at Top
PAGES = {
    "🏠 Landing Page": "index.html",
    "📊 Dashboard": "dashboard.html",
    "🚇 Train Operations": "train-operations.html",
    "✅ Verify Operations": "verify-operations.html",
    "👥 Staff Management": "staff-management.html",
    "📅 Schedule Management": "schedule-management.html",
    "🗺️ Live Route Map": "live-map.html",
    "📈 Reports & Analytics": "reports1.html",
    "🚆 Multitrack Simulation": "multitrack.html",
    "💰 Finance Department": "finance-department.html",
    "🎫 Ticket Booking": "ticket.html",
    "👤 User Portal": "userpage.html",
    "💬 Feedback": "feedback.html",
    "🚦 Control Point Animation": "running.html",
    "📋 Admin Revenue Report": "admin-report.html"
}

# Top Navigation Selector
selected_page_name = st.selectbox(
    "Select Kochi Metro Page:",
    list(PAGES.keys()),
    index=0,
    label_visibility="collapsed"
)

target_file = PAGES[selected_page_name]

if os.path.exists(target_file):
    with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
        html_code = f.read()

    # Render native HTML/CSS/JS frontend directly
    components.html(html_code, height=950, scrolling=True)
else:
    st.error(f"Page file {target_file} not found in project directory.")
