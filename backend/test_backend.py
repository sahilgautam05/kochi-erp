import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("Testing KMRL ERP Backend Endpoints...\n")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print(f"PASS: GET /api/health -> {res.json()['status']}")

    # 2. Rules
    res = client.get("/api/rules")
    assert res.status_code == 200, f"Rules endpoint failed: {res.status_code}"
    data = res.json()
    assert len(data) > 0, "No rules returned"
    print(f"PASS: GET /api/rules -> {len(data)} train rules returned")

    # 3. What-If Defaults
    res = client.get("/api/whatif/defaults")
    assert res.status_code == 200, f"WhatIf defaults failed: {res.status_code}"
    assert "k" in res.json(), "Missing 'k' in defaults"
    print(f"PASS: GET /api/whatif/defaults -> {res.json()}")

    # 4. What-If Optimization
    res = client.post("/api/whatif?k=5&branding_weight=0.5&stabling_weight=0.3")
    assert res.status_code == 200, f"WhatIf calculation failed: {res.status_code}"
    data = res.json()
    assert len(data) == 5, f"Expected 5 results, got {len(data)}"
    print(f"PASS: POST /api/whatif -> Evaluated {len(data)} trains successfully")

    # 5. PDF Reports
    res = client.get("/api/report/status-pdf")
    assert res.status_code == 200, f"Status PDF failed: {res.status_code}"
    assert res.headers["content-type"] == "application/pdf", "Expected application/pdf"
    assert len(res.content) > 1000, "PDF content is too small"
    print(f"PASS: GET /api/report/status-pdf -> {len(res.content)} bytes PDF generated")

    res = client.get("/api/report/whatif-pdf?k=5&branding_weight=0.5&stabling_weight=0.3")
    assert res.status_code == 200, f"WhatIf PDF failed: {res.status_code}"
    assert res.headers["content-type"] == "application/pdf"
    print(f"PASS: GET /api/report/whatif-pdf -> {len(res.content)} bytes PDF generated")

    res = client.get("/api/report/alerts-pdf")
    assert res.status_code == 200, f"Alerts PDF failed: {res.status_code}"
    assert res.headers["content-type"] == "application/pdf"
    print(f"PASS: GET /api/report/alerts-pdf -> {len(res.content)} bytes PDF generated")

    # 6. Trains CRUD
    res = client.get("/api/trains")
    assert res.status_code == 200
    print(f"PASS: GET /api/trains -> {len(res.json())} trains")

    # 7. Staff CRUD
    res = client.get("/api/staff")
    assert res.status_code == 200
    print(f"PASS: GET /api/staff -> {len(res.json())} staff members")

    # 8. Schedules CRUD
    res = client.get("/api/schedules")
    assert res.status_code == 200
    print(f"PASS: GET /api/schedules -> {len(res.json())} schedules")

    # 9. Tickets & Fare Calculation
    res = client.post("/api/tickets/calculate-fare", json={"from": "Aluva", "to": "MG_Road", "passengers": 2})
    assert res.status_code == 200
    fare_data = res.json()
    assert fare_data["total_fare"] == (18 - 1) * 4 * 2, f"Fare calc wrong: {fare_data}"
    print(f"PASS: POST /api/tickets/calculate-fare -> Fare: Rs {fare_data['total_fare']}")

    # 10. Feedback
    res = client.get("/api/feedback/stats")
    assert res.status_code == 200
    print(f"PASS: GET /api/feedback/stats -> Avg Rating: {res.json()['average_rating']}")

    # 11. Revenue
    res = client.get("/api/revenue/summary")
    assert res.status_code == 200
    print(f"PASS: GET /api/revenue/summary -> Total Rev: Rs {res.json()['total_revenue']}")

    # 12. Fleet Prediction
    res = client.post("/api/fleet/predict", json={"dow": 3, "month": 9, "is_weekend": 0, "is_holiday": 0, "special_event": 0, "temp": 28.0})
    assert res.status_code == 200
    fleet_res = res.json()
    assert fleet_res["total_deployed"] == 13
    print(f"PASS: POST /api/fleet/predict -> Total Deployed: {fleet_res['total_deployed']}")

    # 13. Static frontend files
    res = client.get("/")
    assert res.status_code == 200
    assert "Kochi Metro" in res.text
    print("PASS: GET / -> index.html served correctly")

    res = client.get("/dashboard.html")
    assert res.status_code == 200
    print("PASS: GET /dashboard.html -> dashboard.html served correctly")

    res = client.get("/reports1.html")
    assert res.status_code == 200
    print("PASS: GET /reports1.html -> reports1.html served correctly")

    print("\nALL 13 TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
