import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("==================================================")
    print("  Testing KMRL ERP Backend Full Test Suite")
    print("==================================================\n")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print(f"PASS: GET /api/health -> {res.json()['status']}")

    # 2. Rules & What-If Defaults
    res = client.get("/api/rules")
    assert res.status_code == 200, f"Rules endpoint failed: {res.status_code}"
    data = res.json()
    assert len(data) > 0, "No rules returned"
    print(f"PASS: GET /api/rules -> {len(data)} train rules returned")

    res = client.get("/api/whatif/defaults")
    assert res.status_code == 200
    assert "k" in res.json()
    print(f"PASS: GET /api/whatif/defaults -> {res.json()}")

    # 3. What-If Optimization
    res = client.post("/api/whatif?k=5&branding_weight=0.5&stabling_weight=0.3")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 5
    print(f"PASS: POST /api/whatif -> Evaluated {len(data)} trains successfully")

    # 4. PDF Reports
    res = client.get("/api/report/status-pdf")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 1000
    print(f"PASS: GET /api/report/status-pdf -> {len(res.content)} bytes PDF generated")

    res = client.get("/api/report/whatif-pdf?k=5&branding_weight=0.5&stabling_weight=0.3")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    print(f"PASS: GET /api/report/whatif-pdf -> {len(res.content)} bytes PDF generated")

    res = client.get("/api/report/alerts-pdf")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    print(f"PASS: GET /api/report/alerts-pdf -> {len(res.content)} bytes PDF generated")

    # 5. Trains CRUD
    res = client.get("/api/trains")
    assert res.status_code == 200
    trains_list = res.json()
    assert len(trains_list) > 0
    print(f"PASS: GET /api/trains -> {len(trains_list)} trains")

    # Train Update
    train_id = trains_list[0]["id"]
    res = client.put(f"/api/trains/{train_id}", json={"status": "active", "mileage": 55000})
    assert res.status_code == 200
    print(f"PASS: PUT /api/trains/{train_id} -> Updated successfully")

    # 6. Staff CRUD
    res = client.get("/api/staff")
    assert res.status_code == 200
    staff_list = res.json()
    print(f"PASS: GET /api/staff -> {len(staff_list)} staff members")

    # 7. Schedules CRUD
    res = client.get("/api/schedules")
    assert res.status_code == 200
    sched_list = res.json()
    print(f"PASS: GET /api/schedules -> {len(sched_list)} schedules")

    # 8. Tickets & Booking
    res = client.post("/api/tickets/calculate-fare", json={"from": "Aluva", "to": "MG_Road", "passengers": 2})
    assert res.status_code == 200
    fare_data = res.json()
    assert fare_data["total_fare"] == (18 - 1) * 4 * 2
    print(f"PASS: POST /api/tickets/calculate-fare -> Fare: Rs {fare_data['total_fare']}")

    res = client.post("/api/tickets", json={
        "name": "Test Passenger",
        "from": "Aluva",
        "to": "Edapally",
        "passengers": 1,
        "payment": "UPI"
    })
    assert res.status_code == 201
    print(f"PASS: POST /api/tickets -> Ticket #{res.json()['ticket_id']} booked")

    # 9. Feedback Submissions
    res = client.post("/api/feedback", json={
        "name": "Arun Kumar",
        "phone": "+91 98470 11111",
        "rating": 5,
        "comments": "Excellent cleanliness and punctual service."
    })
    assert res.status_code == 201
    print(f"PASS: POST /api/feedback -> Feedback saved")

    res = client.get("/api/feedback/stats")
    assert res.status_code == 200
    print(f"PASS: GET /api/feedback/stats -> Avg Rating: {res.json()['average_rating']}")

    # 10. Finance & Revenue
    res = client.post("/api/revenue", json={
        "company": "Test Sponsor Corp",
        "description": "Digital billboard display advertisement",
        "rupees": 50000.0
    })
    assert res.status_code == 201
    print(f"PASS: POST /api/revenue -> Revenue recorded")

    res = client.get("/api/revenue/summary")
    assert res.status_code == 200
    print(f"PASS: GET /api/revenue/summary -> Total Rev: Rs {res.json()['total_revenue']}")

    # 11. Fleet Simulation & ML Predictions
    res = client.post("/api/fleet/predict", json={"dow": 3, "month": 9, "is_weekend": 0, "is_holiday": 0, "special_event": 0, "temp": 28.0})
    assert res.status_code == 200
    assert res.json()["total_deployed"] == 13
    print(f"PASS: POST /api/fleet/predict -> Total Deployed: {res.json()['total_deployed']}")

    res = client.post("/api/predict/crowd", json={"station": "Edapally", "hour": 18, "dayOfWeek": 1})
    assert res.status_code == 200
    print(f"PASS: POST /api/predict/crowd -> Density: {res.json()['density']}")

    res = client.post("/api/predict/delay", json={"mileage": 30000, "route": "Aluva - Tripunithura", "departureHour": 9})
    assert res.status_code == 200
    print(f"PASS: POST /api/predict/delay -> Delay Risk: {res.json()['delayRiskPercent']}%")

    res = client.post("/api/predict/maintenance", json={"mileage": 40000, "ageMonths": 18, "fitness": 85})
    assert res.status_code == 200
    print(f"PASS: POST /api/predict/maintenance -> Days Remaining: {res.json()['daysRemaining']}")

    # 12. Auth & Storage Sync
    res = client.post("/api/auth/login", json={"username": "admin", "password": "password123", "role": "admin"})
    assert res.status_code == 200
    print(f"PASS: POST /api/auth/login -> Role: {res.json()['role']}")

    res = client.post("/api/storage/test_key", json={"value": "test_val"})
    assert res.status_code == 200
    res = client.get("/api/storage/test_key")
    assert res.status_code == 200
    assert res.json()["value"] == "test_val"
    print(f"PASS: GET/POST /api/storage/test_key -> Sync verified")

    # 13. Verification Tasks
    res = client.get("/api/verification")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) > 0
    res = client.put(f"/api/verification/{tasks[0]['id']}", json={"status": "verified"})
    assert res.status_code == 200
    print(f"PASS: GET/PUT /api/verification -> Tasks verified")

    # 14. Static Frontend Routes
    res = client.get("/")
    assert res.status_code == 200
    assert "Kochi Metro" in res.text
    print("PASS: GET / -> index.html served")

    res = client.get("/dashboard.html")
    assert res.status_code == 200
    print("PASS: GET /dashboard.html -> served")

    res = client.get("/reports1.html")
    assert res.status_code == 200
    print("PASS: GET /reports1.html -> served")

    res = client.get("/live-map.html")
    assert res.status_code == 200
    print("PASS: GET /live-map.html -> served")

    print("\n==================================================")
    print("  ALL 14 TEST SUITES (25+ ENDPOINTS) PASSED!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
