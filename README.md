# Kochi Metro Rail Limited (KMRL) Management System & ERP

A web-based Enterprise Resource Planning (ERP) and operations management platform for Kochi Metro Rail Limited.

---

## 🚇 Features & Modules

- **Dashboard**: High-level overview, service status, real-time KPI metrics, interactive particle animation background.
- **Train Operations**: Monitor and manage active, delayed, and maintenance train rakes with operational telemetry.
- **Verification Operations**: Pre-departure check procedures, maintenance checklists, and status tracking.
- **Staff Management**: Personnel directory, status management (On Duty, Off Duty, On Leave), role assignment, and editing.
- **Schedule Management**: Timetable management, departure/arrival schedules, and CSV export.
- **Live Station Map**: Interactive Leaflet map with real-time train positioning along the Kochi Metro route from Aluva to Tripunithura.
- **Reports & Analytics**: Rule-based eligibility charts, dynamic What-If optimization scenario analysis, alerts breakdown, and downloadable PDF reports.
- **Multitrack Fleet Simulation**: Passenger demand forecasting, weather impact, rake deployment optimizer, and interactive track visualization.
- **Finance & Revenue Portal**: Corporate sponsorship tracking, non-fare revenue entries, fare revenue aggregation, and admin accounting reports.
- **Ticketing & Booking Demo**: Interactive ticket booking, QR-code generation, fare calculation, and e-ticket image download.
- **Customer Feedback & Rating**: Service review submissions, journey satisfaction metrics, and feature polling.

---

## 🚀 Running the Backend

### Prerequisites
- Python 3.9+ (or the pre-configured embedded Python environment)

### Quick Start
Double-click `start_backend.bat` or run:

```bash
# In PowerShell:
./start_backend.ps1

# Or with Python directly:
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Once started:
- **Web App**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative API Docs (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 REST API Summary

### 1. Rules & What-If Optimization
- `GET /api/rules` — Train eligibility status and alert flags for rules engine
- `GET /api/whatif/defaults` — Default weights (`k`, `branding_weight`, `stabling_weight`)
- `POST /api/whatif?k=10&branding_weight=0.5&stabling_weight=0.3` — What-If scenario score simulator

### 2. PDF Reports Generation
- `GET /api/report/status-pdf` — Generates and downloads Train Status & Eligibility Report (PDF)
- `GET /api/report/whatif-pdf` — Generates and downloads What-If Optimization Analysis Report (PDF)
- `GET /api/report/alerts-pdf` — Generates and downloads System Alerts & Faults Report (PDF)

### 3. Operations & Management
- `GET /api/trains`, `POST /api/trains`, `PUT /api/trains/{id}`, `DELETE /api/trains/{id}` — Train fleet CRUD
- `GET /api/staff`, `POST /api/staff`, `PUT /api/staff/{id}`, `DELETE /api/staff/{id}` — Staff management CRUD
- `GET /api/schedules`, `POST /api/schedules`, `PUT /api/schedules/{id}`, `DELETE /api/schedules/{id}` — Timetables CRUD
- `GET /api/tickets`, `POST /api/tickets`, `POST /api/tickets/calculate-fare` — Ticket bookings & fare calculations
- `GET /api/feedback`, `POST /api/feedback`, `GET /api/feedback/stats` — Passenger feedback submissions
- `GET /api/revenue`, `POST /api/revenue`, `GET /api/revenue/summary` — Corporate revenue entries & accounting
- `POST /api/fleet/predict` — Passenger demand prediction and rake deployment optimizer
- `GET /api/verification`, `PUT /api/verification/{task_id}` — Operational verification tasks
- `GET /api/health` — System status & active resource counts