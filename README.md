# Kochi Metro Rail Limited (KMRL) Management System & ERP

A web-based Enterprise Resource Planning (ERP) and operations management platform for Kochi Metro Rail Limited.

---

## 📁 Project Structure

```
kochi-erp/
├── backend/
│   ├── main.py                # FastAPI app, CORS, static file serving & routers
│   ├── database.py            # SQLite database schema, connection & initial KMRL seed data
│   ├── requirements.txt       # Dependencies (FastAPI, Uvicorn, Pydantic, ReportLab)
│   ├── test_backend.py        # Automated test suite for all endpoints
│   └── routes/
│       ├── rules_whatif.py    # Rules engine & What-If optimization scoring
│       ├── reports.py         # Dynamic PDF report generation using ReportLab
│       ├── trains.py          # Train fleet operations CRUD APIs
│       ├── staff.py           # Staff directory & status management CRUD APIs
│       ├── schedules.py       # Timetable and schedules CRUD APIs
│       ├── tickets.py         # Ticket booking, fare calculations & QR generation
│       ├── feedback.py        # Passenger feedback and review analytics
│       ├── finance.py         # Corporate sponsorship & finance portal APIs
│       ├── fleet_ml.py        # Multitrack fleet simulation & predictive ML analytics
│       └── auth_sync.py       # Authentication, verification tasks, and storage sync
├── frontend/
│   ├── index.html             # Landing page & user/admin portal entry
│   ├── dashboard.html         # Executive overview & operational KPIs
│   ├── train-operations.html  # Live train fleet operations & status management
│   ├── verify-operations.html # Pre-trip checklists and verification tasks
│   ├── staff-management.html  # Staff roster and directory
│   ├── schedule-management.html # Timetables, schedules & CSV exports
│   ├── live-map.html          # Interactive Leaflet live route & train map
│   ├── reports1.html          # Dynamic charts & analytics reports
│   ├── multitrack.html        # Multitrack rake predictor & track animations
│   ├── finance-department.html # Revenue entries & financial reporting
│   ├── ticket.html            # E-ticket booking, fare calculation & QR code
│   ├── userpage.html          # Passenger portal & service status
│   ├── feedback.html          # Customer feedback & ratings
│   ├── running.html           # Metro control point simulation
│   └── styles.css             # Comprehensive theme & UI stylesheets
├── requirements.txt           # Unified root dependencies
├── streamlit_app.py           # Streamlit Cloud deployment entrypoint
├── app.py                     # Standard app entrypoint
├── start_backend.bat          # 1-click Windows batch launcher
└── start_backend.ps1          # 1-click PowerShell launcher
```

---

## 🚀 Running the Application

### 1. Run FastAPI Backend (Recommended)
Double-click `start_backend.bat` or run in PowerShell:
```powershell
./start_backend.ps1
```
- **Web App**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Run with Streamlit
```powershell
streamlit run streamlit_app.py
```
- **Streamlit App**: [http://localhost:8501](http://localhost:8501)
