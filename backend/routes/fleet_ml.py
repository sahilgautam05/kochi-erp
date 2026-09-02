from fastapi import APIRouter
from typing import Optional, Dict

router = APIRouter(prefix="/api", tags=["Fleet Simulation & ML Analytics"])

TOTAL_FLEET_SIZE = 40

@router.post("/fleet/predict")
def predict_fleet_deployment(payload: dict):
    """
    Predict passenger demand and optimal train rake allocation across lines.
    Matches the business logic of multitrack fleet management.
    """
    dow = int(payload.get("dow", 3))
    month = int(payload.get("month", 9))
    is_weekend = bool(payload.get("is_weekend", 0))
    is_holiday = bool(payload.get("is_holiday", 0))
    special_event = bool(payload.get("special_event", 0))
    temp = float(payload.get("temp", 28.0))

    line1 = 5
    line2 = 4
    line3 = 4

    if is_weekend:
        line1 += 3
        line2 += 2
        line3 += 2
    if is_holiday:
        line1 += 2
        line2 += 3
        line3 += 3
    if special_event:
        line1 += 2
        line2 += 3
        line3 += 4
    if temp > 35:
        line1 = max(1, line1 - 1)
        line2 = max(1, line2 - 1)

    predictions = {"Line1": line1, "Line2": line2, "Line3": line3}
    total_demand = line1 + line2 + line3

    # Fleet calculations
    maintenance_rakes = 2
    available_fleet = TOTAL_FLEET_SIZE - maintenance_rakes
    reserve_or_shortfall = available_fleet - total_demand

    deployed = {}
    if total_demand <= available_fleet:
        deployed = predictions
    else:
        rem = available_fleet
        deployed["Line1"] = min(line1, rem)
        rem -= deployed["Line1"]
        deployed["Line2"] = min(line2, rem)
        rem -= deployed["Line2"]
        deployed["Line3"] = min(line3, rem)

    total_deployed = sum(deployed.values())

    return {
        "total_fleet": TOTAL_FLEET_SIZE,
        "maintenance_rakes": maintenance_rakes,
        "available_fleet": available_fleet,
        "total_demand": total_demand,
        "total_deployed": total_deployed,
        "reserve_or_shortfall": reserve_or_shortfall,
        "predictions": predictions,
        "deployed_rakes": deployed
    }

@router.post("/predict/crowd")
def predict_crowd(req: dict):
    """
    Predict passenger density and crowd volume at stations.
    """
    station = req.get("station", "Edapally")
    hour = int(req.get("hour", 18))
    day = int(req.get("dayOfWeek", 1))
    event = bool(req.get("event", False))

    # Baseline calculations
    base_count = 500
    if 8 <= hour <= 10 or 17 <= hour <= 20:
        base_count += 750  # Peak commute hours
    if event:
        base_count += 600
    if day in [5, 6]:  # Weekend
        base_count += 200

    density = "Peak Commute" if base_count > 1200 else ("Busy" if base_count > 700 else ("Moderate" if base_count > 350 else "Low"))
    advice = "Increase frequency to 4-min headway" if base_count > 900 else "Standard 7-min headway"

    return {
        "station": station,
        "passengerCount": base_count,
        "density": density,
        "recommendation": advice
    }

@router.post("/predict/delay")
def predict_delay(req: dict):
    """
    Predict likelihood of operational delays for train services.
    """
    mileage = float(req.get("mileage", 25000))
    route_len = 30 if "tripunithura" in str(req.get("route", "")).lower() else 18
    hour = int(req.get("departureHour", 9))
    driver_exp = int(req.get("driverExp", 24))

    risk = int(min(95, max(5, (mileage / 3000.0) + (route_len * 0.4) - (driver_exp * 0.3) + (15 if 8 <= hour <= 10 or 17 <= hour <= 19 else 0))))
    level = "High" if risk > 60 else ("Medium" if risk > 35 else "Low")

    return {
        "delayRiskPercent": risk,
        "riskLevel": level
    }

@router.post("/predict/maintenance")
def predict_maintenance(req: dict):
    """
    Predict equipment wear and remaining operational days before required maintenance.
    """
    mileage = float(req.get("mileage", 25000))
    age = int(req.get("ageMonths", 12))
    fitness = float(req.get("fitness", 90))
    alerts = int(req.get("activeAlerts", 0))

    prob = int(min(98, max(5, (mileage / 2000.0) + (age * 1.2) + (alerts * 15) - (fitness * 0.4))))
    days = int(max(2, 90 - (prob * 0.8)))

    return {
        "breakdownProbability": prob,
        "daysRemaining": days,
        "status": "Critical" if prob > 65 else ("Maintenance Due" if prob > 35 else "Healthy"),
        "wear": {
            "wheel": f"{min((mileage / 18000) * 1.5, 3.0):.2f} mm",
            "panto": f"{min((mileage / 10000) * 1.2, 5.0):.2f} mm"
        }
    }
