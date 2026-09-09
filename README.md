# 🚇 Kochi Metro Rail Limited (KMRL) Management System & ERP

[![Live Demo on Vercel](https://img.shields.io/badge/Live%20Demo-Vercel%20Deployment-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://kochi-erp-62tz.vercel.app/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-sahilgautam05%2Fkochi--erp-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sahilgautam05/kochi-erp)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

An enterprise-grade web platform and operations management ERP developed for **Kochi Metro Rail Limited (KMRL)**.

🔗 **Live Production URL**: [https://kochi-erp-62tz.vercel.app/](https://kochi-erp-62tz.vercel.app/)

---

## 🌟 Key Features & Modules

- 🌐 **Live Production Deployment**: Hosted on Vercel with serverless backend APIs at [https://kochi-erp-62tz.vercel.app/](https://kochi-erp-62tz.vercel.app/).
- 📊 **Executive Dashboard**: High-level KPIs, real-time ridership analytics, and operational compliance.
- 🚇 **Train Fleet Operations**: Live rake tracking, fitness verification, job cards, bay assignments, and status filtering.
- 🗺️ **Live Station & Route Map**: Real-time Leaflet map tracking train movement across all 25 stations from Aluva to Tripunithura.
- 📈 **Rules-Based Engine & What-If Optimizer**: Multi-objective scenario optimization evaluating mileage, branding, and stabling efficiency with dynamic charts.
- 📄 **Official PDF Reports**: Dynamic generation and download of Status Compliance, What-If Analysis, and Alerts Distribution PDF reports via ReportLab.
- 🚆 **Multitrack Simulation & ML Demand Forecasting**: Weather-aware passenger demand predictor and rake deployment optimizer across 3 metro lines.
- 🎫 **Ticketing & Automated Email Dispatch**: Online ticket booking, fare estimation (₹4/km), QR-code generation, and automated branded e-ticket delivery directly to the passenger's email address.
- 👥 **Staff Management**: Personnel directory, role assignments (Train Drivers, Station Managers, Technicians), and duty status tracking.
- 📅 **Schedule Management**: Timetable management, departure/arrival schedules, and CSV export.
- 💰 **Finance & Revenue Portal**: Non-fare sponsorship management and financial aggregation.
- 💬 **Customer Feedback & Review**: Passenger ratings, feature polling, and satisfaction metrics.

---

## 📁 Project Architecture

```
kochi-erp/
├── api/
│   └── index.py               # Vercel Serverless Function entrypoint
├── backend/
│   ├── main.py                # FastAPI app, CORS, static file routing
│   ├── database.py            # SQLite database models & seed data
│   ├── email_service.py       # Branded e-Ticket email generation & delivery
│   ├── requirements.txt       # Backend dependencies
│   ├── test_backend.py        # Automated test suite (14 suites, 25+ endpoints)
│   └── routes/
│       ├── rules_whatif.py    # Rules engine & What-If optimization
│       ├── reports.py         # Dynamic PDF report generation (ReportLab)
│       ├── trains.py          # Train operations CRUD APIs
│       ├── staff.py           # Staff directory & status CRUD APIs
│       ├── schedules.py       # Timetable & schedule CRUD APIs
│       ├── tickets.py         # Ticket booking & email dispatch
│       ├── feedback.py        # Passenger feedback & ratings
│       ├── finance.py         # Sponsorship revenue & accounting
│       ├── fleet_ml.py        # Fleet simulation & ML analytics
│       └── auth_sync.py       # Authentication, verification & storage sync
├── frontend/
│   ├── index.html             # Landing page & login modal
│   ├── dashboard.html         # Executive overview & KPIs
│   ├── train-operations.html  # Fleet status & train cards
│   ├── verify-operations.html # Operational checklists
│   ├── staff-management.html  # Staff directory
│   ├── schedule-management.html # Timetables & CSV export
│   ├── live-map.html          # Interactive Leaflet live route map
│   ├── reports1.html          # Dynamic charts & PDF downloads
│   ├── multitrack.html        # ML rake demand predictor
│   ├── finance-department.html # Revenue entries & reports
│   ├── ticket.html            # E-ticket booking with email delivery
│   ├── userpage.html          # Passenger portal
│   ├── feedback.html          # Passenger reviews
│   ├── running.html           # Metro control point simulation
│   └── styles.css             # Theme stylesheets
├── vercel.json                # Vercel Serverless deployment configuration
├── requirements.txt           # Unified Python dependencies
├── streamlit_app.py           # Streamlit Cloud deployment entrypoint
├── app.py                     # Root entrypoint
├── start_backend.bat          # 1-click Windows batch launcher
└── start_backend.ps1          # 1-click PowerShell launcher
```

---

## 🚀 Running Locally

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

### 3. Run Automated Tests
```powershell
python backend/test_backend.py
```

---

## 🌐 Cloud Deployments

- **Vercel**: [https://kochi-erp-62tz.vercel.app/](https://kochi-erp-62tz.vercel.app/)
- **GitHub Repository**: [https://github.com/sahilgautam05/kochi-erp](https://github.com/sahilgautam05/kochi-erp)
