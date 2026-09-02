import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import re
import base64
import threading
import time

# Page configuration
st.set_page_config(
    page_title="Kochi Metro Rail Limited (KMRL) ERP",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Start background FastAPI server if available
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend") if os.path.exists(os.path.join(BASE_DIR, "frontend")) else BASE_DIR
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

def start_backend():
    try:
        import uvicorn
        from main import app
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
    except Exception as e:
        pass

if "backend_thread_started" not in st.session_state:
    try:
        t = threading.Thread(target=start_backend, daemon=True)
        t.start()
        st.session_state["backend_thread_started"] = True
    except Exception:
        pass

# Clean CSS to remove padding and ensure full-height bright display
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    .stSelectbox {
        margin-bottom: 0.5rem;
    }
    iframe {
        width: 100% !important;
        min-height: 960px !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        background: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Mapping
PAGES = {
    "🏠 Landing Page": "index.html",
    "📊 Executive Dashboard": "dashboard.html",
    "🚇 Train Fleet Operations": "train-operations.html",
    "➕ Add Train": "add-train.html",
    "✅ Verification Operations": "verify-operations.html",
    "👥 Staff Management": "staff-management.html",
    "➕ Add Staff": "add-staff.html",
    "📅 Schedule Management": "schedule-management.html",
    "➕ Add Schedule": "add-schedule.html",
    "🗺️ Live Route & Station Map": "live-map.html",
    "📈 Reports & Optimization Charts": "reports1.html",
    "🚆 Multitrack Simulation": "multitrack.html",
    "💰 Finance & Sponsorship Department": "finance-department.html",
    "🎫 Ticket Booking & QR Fare Calculator": "ticket.html",
    "👤 Passenger Portal": "userpage.html",
    "💬 Passenger Feedback": "feedback.html",
    "🚦 Control Point Simulation": "running.html",
    "📋 Admin Revenue Report": "admin-report.html"
}

# Top Navigation Control
col_title, col_nav = st.columns([1, 2])
with col_title:
    st.markdown("### 🚇 **Kochi Metro Rail Limited**")
with col_nav:
    selected_page_label = st.selectbox(
        "Navigation",
        list(PAGES.keys()),
        index=0,
        label_visibility="collapsed"
    )

target_filename = PAGES[selected_page_label]
target_path = os.path.join(FRONTEND_DIR, target_filename)

def get_inlined_html(filepath):
    if not os.path.exists(filepath):
        return f"<div style='padding:20px; font-family:sans-serif;'><h2>File {os.path.basename(filepath)} not found</h2></div>"

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # 1. Inline CSS files
    def inline_css(m):
        css_name = m.group(1)
        full_css = os.path.join(FRONTEND_DIR, css_name)
        if os.path.exists(full_css):
            with open(full_css, "r", encoding="utf-8", errors="ignore") as cf:
                return f"<style>\n{cf.read()}\n</style>"
        return m.group(0)

    html = re.sub(r'<link\s+[^>]*href=["\']([^"\']+\.css)["\'][^>]*>', inline_css, html, flags=re.IGNORECASE)

    # 2. Inline JavaScript files
    def inline_js(m):
        js_name = m.group(1)
        full_js = os.path.join(FRONTEND_DIR, js_name)
        if os.path.exists(full_js):
            with open(full_js, "r", encoding="utf-8", errors="ignore") as jf:
                return f"<script>\n{jf.read()}\n</script>"
        return m.group(0)

    html = re.sub(r'<script\s+[^>]*src=["\']([^"\']+\.js)["\'][^>]*>\s*</script>', inline_js, html, flags=re.IGNORECASE)

    # 3. Inline images in src="..."
    def inline_img_src(m):
        img_name = m.group(1)
        full_img = os.path.join(FRONTEND_DIR, img_name)
        if os.path.exists(full_img):
            ext = os.path.splitext(img_name)[1].lower()
            mime = "image/png" if ext == ".png" else ("image/svg+xml" if ext == ".svg" else "image/jpeg")
            with open(full_img, "rb") as imf:
                b64 = base64.b64encode(imf.read()).decode("utf-8")
            return f'src="data:{mime};base64,{b64}"'
        return m.group(0)

    html = re.sub(r'src=["\']([a-zA-Z0-9_\-]+\.(?:jpg|jpeg|png|webp|svg))["\']', inline_img_src, html, flags=re.IGNORECASE)

    # 4. Inline CSS background-image url(...)
    def inline_css_url(m):
        img_name = m.group(1).strip('\'"')
        full_img = os.path.join(FRONTEND_DIR, img_name)
        if os.path.exists(full_img):
            ext = os.path.splitext(img_name)[1].lower()
            mime = "image/png" if ext == ".png" else ("image/svg+xml" if ext == ".svg" else "image/jpeg")
            with open(full_img, "rb") as imf:
                b64 = base64.b64encode(imf.read()).decode("utf-8")
            return f'url("data:{mime};base64,{b64}")'
        return m.group(0)

    html = re.sub(r'url\((["\']?[a-zA-Z0-9_\-]+\.(?:jpg|jpeg|png|webp|svg)["\']?)\)', inline_css_url, html, flags=re.IGNORECASE)

    return html

# Generate fully self-contained HTML bundle
inlined_content = get_inlined_html(target_path)

# Render inside Streamlit component
components.html(inlined_content, height=1000, scrolling=True)
