import os
import sys

# Ensure backend directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend") if os.path.exists(os.path.join(ROOT_DIR, "frontend")) else ROOT_DIR

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from database import init_db
from routes import (
    rules_whatif,
    reports,
    trains,
    staff,
    schedules,
    tickets,
    feedback,
    finance,
    fleet_ml,
    auth_sync
)

# Initialize database tables and seed data
init_db()

app = FastAPI(
    title="Kochi Metro Rail Limited (KMRL) ERP Backend",
    description="Comprehensive Enterprise Backend APIs for Kochi Metro Operations, Ticketing, Fleet, and Analytics.",
    version="2.0.0"
)

# Enable CORS for all origins so any frontend client can connect seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All API Routers
app.include_router(rules_whatif.router)
app.include_router(reports.router)
app.include_router(trains.router)
app.include_router(staff.router)
app.include_router(schedules.router)
app.include_router(tickets.router)
app.include_router(feedback.router)
app.include_router(finance.router)
app.include_router(fleet_ml.router)
app.include_router(auth_sync.router)

# Custom Route to serve the Landing Page at root /
@app.get("/")
def root():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h2>Kochi Metro ERP Backend is Running</h2>")

# Serve all frontend static files (.html, .css, .js, .jpg, etc.) directly from FRONTEND_DIR
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("  Kochi Metro Rail Management System - Backend Server")
    print("  Running on: http://127.0.0.1:8000")
    print("  API Docs:   http://127.0.0.1:8000/docs")
    print("=" * 60)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
