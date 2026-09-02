import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import io
import sys
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Kochi Metro Rail Limited (KMRL) ERP",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-left: 5px solid #2563eb;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .badge-active {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-delayed {
        background-color: #fef9c3;
        color: #854d0e;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-maintenance {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Station Coordinates along Kochi Metro Route (Aluva -> Tripunithura)
STATIONS_DATA = [
    {"name": "Aluva", "lat": 10.1114, "lon": 76.3516, "distance": 18},
    {"name": "Pulinchodu", "lat": 10.1018, "lon": 76.3482, "distance": 16},
    {"name": "Companypady", "lat": 10.0925, "lon": 76.3450, "distance": 15},
    {"name": "Ambattukavu", "lat": 10.0833, "lon": 76.3395, "distance": 14},
    {"name": "Muttom", "lat": 10.0734, "lon": 76.3363, "distance": 13},
    {"name": "Kalamassery", "lat": 10.0593, "lon": 76.3260, "distance": 12},
    {"name": "CUSAT", "lat": 10.0486, "lon": 76.3208, "distance": 11},
    {"name": "Pathadipalam", "lat": 10.0375, "lon": 76.3128, "distance": 10},
    {"name": "Edapally", "lat": 10.0259, "lon": 76.3087, "distance": 9},
    {"name": "Changampuzha Park", "lat": 10.0160, "lon": 76.3041, "distance": 8},
    {"name": "Palarivattom", "lat": 10.0102, "lon": 76.2999, "distance": 6},
    {"name": "JLN Stadium", "lat": 9.9993, "lon": 76.2986, "distance": 5},
    {"name": "Kaloor", "lat": 9.9872, "lon": 76.2952, "distance": 2},
    {"name": "Town Hall / Lissie", "lat": 9.9816, "lon": 76.2906, "distance": 0},
    {"name": "M.G. Road", "lat": 9.9762, "lon": 76.2857, "distance": 1},
    {"name": "Maharajas College", "lat": 9.9698, "lon": 76.2807, "distance": 4},
    {"name": "Ernakulam South", "lat": 9.9574, "lon": 76.2765, "distance": 5},
    {"name": "Kadavanthra", "lat": 9.9507, "lon": 76.2762, "distance": 3},
    {"name": "Elamkulam", "lat": 9.9411, "lon": 76.2760, "distance": 5},
    {"name": "Vyttila", "lat": 9.9323, "lon": 76.2800, "distance": 7},
    {"name": "Thaikoodam", "lat": 9.9244, "lon": 76.2953, "distance": 9},
    {"name": "Pettah", "lat": 9.9182, "lon": 76.3025, "distance": 10},
    {"name": "Vadakkekotta", "lat": 9.9170, "lon": 76.3105, "distance": 11},
    {"name": "SN Junction", "lat": 9.9160, "lon": 76.3185, "distance": 12},
    {"name": "Tripunithura", "lat": 9.9141, "lon": 76.3262, "distance": 14}
]

# Initialize Session State Data
if "trains" not in st.session_state:
    st.session_state.trains = [
        {"id": "K101", "name": "Kochi Express", "route": "Aluva - Tripunithura", "driver": "Rajesh Kumar", "next": "Edappally", "status": "active", "fitness": "Certified OK", "jobCard": "Completed", "mileage": 54200, "branding": "Adani Group", "bay": "Bay 04"},
        {"id": "K102", "name": "Periyar Voyager", "route": "Tripunithura - Aluva", "driver": "Priya Nair", "next": "Kakkanad", "status": "delayed", "fitness": "Certified OK", "jobCard": "Pending", "mileage": 71340, "branding": "Lulu Group", "bay": "Track 2"},
        {"id": "K103", "name": "Marine Drive Metro", "route": "Aluva - Tripunithura", "driver": "Suresh Babu", "next": "Kaloor", "status": "active", "fitness": "Certified OK", "jobCard": "Completed", "mileage": 32100, "branding": "Muthoot Finance", "bay": "Bay 01"},
        {"id": "K104", "name": "Depot Unit 04", "route": "Maintenance Mode", "driver": "N/A", "next": "Depot", "status": "maintenance", "fitness": "Under Inspection", "jobCard": "In Progress", "mileage": 120500, "branding": "None", "bay": "Depot Bay 1"},
        {"id": "K105", "name": "Queen of Arabian Sea", "route": "Tripunithura - Aluva", "driver": "Meera Thomas", "next": "Palarivattom", "status": "active", "fitness": "Certified OK", "jobCard": "Completed", "mileage": 48900, "branding": "Federal Bank", "bay": "Bay 03"},
        {"id": "K106", "name": "Vembanad Flyer", "route": "Aluva - Tripunithura", "driver": "Ravi Menon", "next": "M.G. Road", "status": "active", "fitness": "Certified OK", "jobCard": "Completed", "mileage": 61200, "branding": "Aster DM", "bay": "Bay 02"}
    ]

if "staff" not in st.session_state:
    st.session_state.staff = [
        {"id": "EMP001", "name": "Rajesh Kumar", "role": "Train Driver", "status": "On Duty", "phone": "+91 98470 12345"},
        {"id": "EMP002", "name": "Priya Nair", "role": "Train Driver", "status": "On Duty", "phone": "+91 98470 23456"},
        {"id": "EMP003", "name": "Suresh Babu", "role": "Station Manager", "status": "On Duty", "phone": "+91 98470 34567"},
        {"id": "EMP004", "name": "Arun Krishnan", "role": "Maintenance Technician", "status": "On Duty", "phone": "+91 98470 45678"},
        {"id": "EMP005", "name": "Meera Thomas", "role": "Train Driver", "status": "On Duty", "phone": "+91 98470 56789"},
        {"id": "EMP006", "name": "Ravi Menon", "role": "Control Room Operator", "status": "On Duty", "phone": "+91 98470 67890"},
        {"id": "EMP007", "name": "Ananya Pillai", "role": "Customer Service", "status": "On Duty", "phone": "+91 98470 78901"},
        {"id": "EMP008", "name": "Kavitha Varma", "role": "Security Officer", "status": "Off Duty", "phone": "+91 98470 89012"}
    ]

if "schedules" not in st.session_state:
    st.session_state.schedules = [
        {"train_id": "K101", "route": "Aluva - Tripunithura", "departure": "06:00 AM", "arrival": "06:45 AM", "driver": "Rajesh Kumar", "status": "Operational"},
        {"train_id": "K102", "route": "Tripunithura - Aluva", "departure": "06:30 AM", "arrival": "07:15 AM", "driver": "Priya Nair", "status": "Delayed"},
        {"train_id": "K103", "route": "Aluva - Tripunithura", "departure": "07:00 AM", "arrival": "07:45 AM", "driver": "Suresh Babu", "status": "Operational"},
        {"train_id": "K104", "route": "Maintenance Mode", "departure": "-", "arrival": "-", "driver": "N/A", "status": "Maintenance"},
        {"train_id": "K105", "route": "Tripunithura - Aluva", "departure": "07:30 AM", "arrival": "08:15 AM", "driver": "Meera Thomas", "status": "Operational"},
        {"train_id": "K106", "route": "Aluva - Tripunithura", "departure": "08:00 AM", "arrival": "08:45 AM", "driver": "Ravi Menon", "status": "Operational"}
    ]

if "tickets" not in st.session_state:
    st.session_state.tickets = [
        {"name": "John Doe", "from": "Aluva", "to": "M.G. Road", "fare": 68.0, "passengers": 1, "date": "02/09/2026"},
        {"name": "Aisha Rahman", "from": "Edapally", "to": "Vyttila", "fare": 32.0, "passengers": 2, "date": "02/09/2026"},
        {"name": "Vikram Singh", "from": "Kaloor", "to": "Tripunithura", "fare": 48.0, "passengers": 1, "date": "02/09/2026"}
    ]

# Sidebar Navigation
st.sidebar.image("logo1.jpg" if os.path.exists("logo1.jpg") else "logo.jpg", width=180)
st.sidebar.title("KMRL Portal")
nav = st.sidebar.radio(
    "Navigation Menu",
    [
        "📊 Dashboard & Overview",
        "🚇 Train Operations",
        "🗺️ Live Metro Map",
        "👥 Staff Management",
        "📅 Timetables & Schedules",
        "📈 Rules & What-If Optimizer",
        "📄 PDF Reports Center",
        "🚆 Multitrack Fleet Predictor",
        "🎫 Ticket Booking & QR",
        "💰 Corporate Finance",
        "💬 Passenger Feedback",
        "🌐 Web Frontend Portal"
    ]
)

# -------------------------------------------------------------
# 1. DASHBOARD & OVERVIEW
# -------------------------------------------------------------
if nav == "📊 Dashboard & Overview":
    st.markdown('<div class="main-header">🚇 Kochi Metro Rail Limited</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enterprise Operations, Fleet Management & Passenger Telemetry System</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Stations", "25 Active", "+3 Under Phase 2")
    with col2:
        st.metric("Daily Passengers", "120,450", "+8.2% vs last month")
    with col3:
        st.metric("On-Time Performance", "99.4%", "0.2% variance")
    with col4:
        st.metric("Total Route Length", "27.96 km", "Aluva to Tripunithura")

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("Hourly Passenger Ridership Distribution")
        hours = [f"{h:02d}:00" for h in range(6, 23)]
        ridership = [1200, 3800, 8900, 11400, 7200, 5400, 4900, 5200, 6100, 7800, 12800, 13400, 9200, 6800, 4500, 2900, 1100]
        fig_ridership = px.area(
            x=hours, y=ridership,
            labels={"x": "Time of Day", "y": "Passengers"},
            color_discrete_sequence=["#2563eb"]
        )
        fig_ridership.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_ridership, use_container_width=True)

    with col_right:
        st.subheader("Fleet Operating Status")
        status_counts = pd.DataFrame(st.session_state.trains)["status"].value_counts()
        fig_pie = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            color=status_counts.index,
            color_discrete_map={"active": "#10b981", "delayed": "#f59e0b", "maintenance": "#ef4444"},
            hole=0.4
        )
        fig_pie.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------------------------------------
# 2. TRAIN OPERATIONS
# -------------------------------------------------------------
elif nav == "🚇 Train Operations":
    st.markdown('<div class="main-header">Train Fleet Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Live rake monitoring, operational telemetry, and bay management</div>', unsafe_allow_html=True)

    filter_opt = st.selectbox("Filter Status", ["All", "active", "delayed", "maintenance"])
    search_q = st.text_input("🔍 Search Trains (by ID, Driver, Route)")

    trains_df = pd.DataFrame(st.session_state.trains)
    if filter_opt != "All":
        trains_df = trains_df[trains_df["status"] == filter_opt]
    if search_q:
        trains_df = trains_df[trains_df.apply(lambda row: search_q.lower() in str(row.values).lower(), axis=1)]

    for idx, row in trains_df.iterrows():
        with st.expander(f"🚆 {row['id']} — {row['name']} ({row['status'].upper()})", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            c1.write(f"**Route**: {row['route']}")
            c1.write(f"**Driver**: {row['driver']}")
            c2.write(f"**Next Station**: {row['next']}")
            c2.write(f"**Bay Position**: {row['bay']}")
            c3.write(f"**Fitness**: {row['fitness']}")
            c3.write(f"**Job Card**: {row['jobCard']}")
            c4.write(f"**Mileage**: {row['mileage']:,} km")
            c4.write(f"**Branding Partner**: {row['branding']}")

# -------------------------------------------------------------
# 3. LIVE METRO MAP
# -------------------------------------------------------------
elif nav == "🗺️ Live Metro Map":
    st.markdown('<div class="main-header">Live Network & Station Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Real-time geospatial visualization of all 25 Kochi Metro stations</div>', unsafe_allow_html=True)

    map_df = pd.DataFrame(STATIONS_DATA)
    fig_map = px.scatter_mapbox(
        map_df,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data={"distance": True, "lat": False, "lon": False},
        color_discrete_sequence=["#2563eb"],
        zoom=11.5,
        height=500
    )
    fig_map.add_trace(go.Scattermapbox(
        mode="lines",
        lat=map_df["lat"],
        lon=map_df["lon"],
        line=dict(width=4, color="#1e3a8a"),
        name="Kochi Metro Line 1"
    ))
    fig_map.update_layout(
        mapbox_style="carto-positron",
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Station Directory")
    st.dataframe(map_df[["name", "distance", "lat", "lon"]], use_container_width=True)

# -------------------------------------------------------------
# 4. STAFF MANAGEMENT
# -------------------------------------------------------------
elif nav == "👥 Staff Management":
    st.markdown('<div class="main-header">Staff & Personnel Directory</div>', unsafe_allow_html=True)
    staff_df = pd.DataFrame(st.session_state.staff)
    st.dataframe(staff_df, use_container_width=True)

    with st.form("add_staff_form"):
        st.subheader("Add New Staff Member")
        name = st.text_input("Full Name")
        emp_id = st.text_input("Employee ID (e.g. EMP009)")
        role = st.selectbox("Department / Role", ["Train Driver", "Station Manager", "Maintenance Technician", "Security Officer", "Customer Service", "Control Room Operator"])
        status = st.selectbox("Duty Status", ["On Duty", "Off Duty", "On Leave"])
        phone = st.text_input("Phone Number")
        submitted = st.form_submit_button("Save Staff Member")
        if submitted and name and emp_id:
            st.session_state.staff.append({"id": emp_id, "name": name, "role": role, "status": status, "phone": phone})
            st.success(f"Staff {name} added successfully!")
            st.rerun()

# -------------------------------------------------------------
# 5. TIMETABLES & SCHEDULES
# -------------------------------------------------------------
elif nav == "📅 Timetables & Schedules":
    st.markdown('<div class="main-header">Train Timetables & Schedules</div>', unsafe_allow_html=True)
    sched_df = pd.DataFrame(st.session_state.schedules)
    st.dataframe(sched_df, use_container_width=True)

    csv = sched_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Schedule as CSV", data=csv, file_name="kochi_metro_schedules.csv", mime="text/csv")

# -------------------------------------------------------------
# 6. RULES & WHAT-IF OPTIMIZER
# -------------------------------------------------------------
elif nav == "📈 Rules & What-If Optimizer":
    st.markdown('<div class="main-header">Rules-Based Engine & What-If Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Dynamic multi-objective optimization comparing baseline mileage vs optimization scores</div>', unsafe_allow_html=True)

    col_k, col_bw, col_sw = st.columns(3)
    with col_k:
        k_val = st.slider("Top K Trains to Evaluate", 1, 10, 6)
    with col_bw:
        bw_val = st.slider("Branding Weight", 0.0, 1.0, 0.5, 0.1)
    with col_sw:
        sw_val = st.slider("Stabling Efficiency Weight", 0.0, 1.0, 0.3, 0.1)

    eval_data = []
    for t in st.session_state.trains[:k_val]:
        base_mileage = t["mileage"]
        norm_mileage = max(10.0, 100.0 - (base_mileage / 1500.0))
        brand_score = 20.0 if t["branding"] != "None" else 5.0
        stabling_score = 15.0 if "Bay" in t["bay"] else 8.0
        score = round((norm_mileage * 0.5) + (brand_score * bw_val * 2.0) + (stabling_score * sw_val * 2.0), 2)
        eval_data.append({
            "Train ID": t["id"],
            "Train Name": t["name"],
            "Baseline Mileage (km)": base_mileage,
            "Optimized Score": score,
            "Branding": t["branding"],
            "Stabling": t["bay"]
        })

    eval_df = pd.DataFrame(eval_data)
    fig_bar = px.bar(
        eval_df,
        x="Train ID",
        y="Optimized Score",
        color="Optimized Score",
        color_continuous_scale="Blues",
        text_auto=True,
        title="Optimization Scores after What-If Simulation"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.dataframe(eval_df, use_container_width=True)

# -------------------------------------------------------------
# 7. PDF REPORTS CENTER
# -------------------------------------------------------------
elif nav == "📄 PDF Reports Center":
    st.markdown('<div class="main-header">KMRL PDF Reports Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Download official formatted PDF reports generated by backend engine</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Train Status Report")
        st.write("Fleet eligibility, compliance and maintenance status.")
        if st.button("Generate Status PDF"):
            try:
                from routes.reports import generate_status_pdf
                pdf_res = generate_status_pdf()
                st.download_button("📥 Download Status PDF", data=pdf_res.body, file_name="kmrl-status-report.pdf", mime="application/pdf")
            except Exception:
                st.info("Direct PDF download ready via backend API endpoint: `/api/report/status-pdf`")

    with c2:
        st.subheader("What-If Analysis Report")
        st.write("Optimization comparison and scoring results.")
        if st.button("Generate What-If PDF"):
            try:
                from routes.reports import generate_whatif_pdf
                pdf_res = generate_whatif_pdf(k=6, branding_weight=0.5, stabling_weight=0.3)
                st.download_button("📥 Download What-If PDF", data=pdf_res.body, file_name="kmrl-whatif-report.pdf", mime="application/pdf")
            except Exception:
                st.info("Direct PDF download ready via backend API endpoint: `/api/report/whatif-pdf`")

    with c3:
        st.subheader("Alerts Distribution Report")
        st.write("Breakdown of system alerts and fault warnings.")
        if st.button("Generate Alerts PDF"):
            try:
                from routes.reports import generate_alerts_pdf
                pdf_res = generate_alerts_pdf()
                st.download_button("📥 Download Alerts PDF", data=pdf_res.body, file_name="kmrl-alerts-report.pdf", mime="application/pdf")
            except Exception:
                st.info("Direct PDF download ready via backend API endpoint: `/api/report/alerts-pdf`")

# -------------------------------------------------------------
# 8. MULTITRACK FLEET PREDICTOR
# -------------------------------------------------------------
elif nav == "🚆 Multitrack Fleet Predictor":
    st.markdown('<div class="main-header">Multitrack Fleet Deployment Predictor</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        dow = st.selectbox("Day of Week", [0, 1, 2, 3, 4, 5, 6], index=3)
        temp = st.slider("Temperature (°C)", 20.0, 45.0, 28.0)
    with c2:
        is_weekend = st.checkbox("Weekend")
        is_holiday = st.checkbox("Holiday")
    with c3:
        special_event = st.checkbox("Special Event in City")

    l1, l2, l3 = 5, 4, 4
    if is_weekend: l1 += 3; l2 += 2; l3 += 2
    if is_holiday: l1 += 2; l2 += 3; l3 += 3
    if special_event: l1 += 2; l2 += 3; l3 += 4
    if temp > 35: l1 = max(1, l1 - 1); l2 = max(1, l2 - 1)

    total_req = l1 + l2 + l3
    st.metric("Total Rakes Required", f"{total_req} Rakes", f"Line 1: {l1} | Line 2: {l2} | Line 3: {l3}")

# -------------------------------------------------------------
# 9. TICKET BOOKING & QR
# -------------------------------------------------------------
elif nav == "🎫 Ticket Booking & QR":
    st.markdown('<div class="main-header">Ticketing & Fare Calculation</div>', unsafe_allow_html=True)

    station_names = [s["name"] for s in STATIONS_DATA]
    c1, c2 = st.columns(2)
    with c1:
        from_st = st.selectbox("Departure Station", station_names, index=0)
    with c2:
        to_st = st.selectbox("Destination Station", station_names, index=12)

    passengers = st.number_input("Number of Passengers", 1, 10, 1)
    pass_name = st.text_input("Passenger Name", "Sahil Gautam")

    d1 = next(s["distance"] for s in STATIONS_DATA if s["name"] == from_st)
    d2 = next(s["distance"] for s in STATIONS_DATA if s["name"] == to_st)
    dist = abs(d1 - d2)
    fare = dist * 4 * passengers

    st.info(f"📍 Distance: **{dist} km** | Total Fare: **₹{fare:.2f}** (₹4/km)")

    if st.button("🎟️ Generate e-Ticket"):
        st.session_state.tickets.append({
            "name": pass_name,
            "from": from_st,
            "to": to_st,
            "fare": fare,
            "passengers": passengers,
            "date": datetime.now().strftime("%d/%m/%Y")
        })
        st.success(f"e-Ticket Generated for {pass_name}!")

# -------------------------------------------------------------
# 10. CORPORATE FINANCE
# -------------------------------------------------------------
elif nav == "💰 Corporate Finance":
    st.markdown('<div class="main-header">Finance & Corporate Sponsorships</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Total Corporate Sponsorships", "₹1,050,000.00", "3 Active Contracts")
    c2.metric("Ticketing Revenue", "₹185,420.00", "Live Farebox Collections")

# -------------------------------------------------------------
# 11. PASSENGER FEEDBACK
# -------------------------------------------------------------
elif nav == "💬 Passenger Feedback":
    st.markdown('<div class="main-header">Passenger Feedback & Satisfaction</div>', unsafe_allow_html=True)
    st.metric("Overall Satisfaction Rating", "4.8 / 5.0 ⭐", "Based on 1,420 passenger ratings")

# -------------------------------------------------------------
# 12. WEB FRONTEND PORTAL
# -------------------------------------------------------------
elif nav == "🌐 Web Frontend Portal":
    st.markdown('<div class="main-header">Native Web Frontend Preview</div>', unsafe_allow_html=True)
    page = st.selectbox("Select Page to Preview", [
        "index.html", "dashboard.html", "reports1.html", "train-operations.html",
        "staff-management.html", "schedule-management.html", "ticket.html",
        "multitrack.html", "live-map.html", "finance-department.html", "feedback.html"
    ])
    if os.path.exists(page):
        with open(page, "r", encoding="utf-8", errors="ignore") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=800, scrolling=True)
