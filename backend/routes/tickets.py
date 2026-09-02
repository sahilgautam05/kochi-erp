from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/api/tickets", tags=["Ticketing & Booking"])

STATIONS = {
    "Aluva": 18,
    "Edapally": 11,
    "Ernakulam_Jn": 9,
    "Palarivattom": 6,
    "Maharajas": 4,
    "Kaloor": 2,
    "Lissie": 0,
    "MG_Road": 1,
    "Kadavanthra": 3,
    "Elamkulam": 5,
    "Vyttila": 7,
    "Edakochi": 13,
}

FARE_PER_KM = 4

@router.post("/calculate-fare")
def calculate_fare(payload: dict):
    from_st = payload.get("from") or payload.get("from_station")
    to_st = payload.get("to") or payload.get("to_station")
    passengers = int(payload.get("passengers", 1) or 1)

    if not from_st or not to_st:
        raise HTTPException(status_code=400, detail="Departure and Destination stations are required")

    d1 = STATIONS.get(from_st, 0)
    d2 = STATIONS.get(to_st, 0)
    distance = abs(d1 - d2)
    total_fare = distance * FARE_PER_KM * passengers

    return {
        "from": from_st,
        "to": to_st,
        "distance_km": distance,
        "passengers": passengers,
        "fare_per_km": FARE_PER_KM,
        "total_fare": float(total_fare)
    }

@router.get("")
def list_tickets():
    """List all booked tickets."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        results.append({
            "id": d["id"],
            "name": d["passenger_name"],
            "passenger_name": d["passenger_name"],
            "from": d["from_station"],
            "from_station": d["from_station"],
            "to": d["to_station"],
            "to_station": d["to_station"],
            "distance": d["distance_km"],
            "distance_km": d["distance_km"],
            "passengers": d["passengers"],
            "fare": d["fare"],
            "payment": d["payment_method"],
            "payment_method": d["payment_method"],
            "date": d["ticket_date"],
            "ticket_date": d["ticket_date"],
            "time": d["ticket_time"],
            "ticket_time": d["ticket_time"],
            "qr_data": d["qr_data"]
        })
    return results

@router.post("", status_code=201)
def book_ticket(payload: dict):
    """Book a new metro ticket."""
    name = (payload.get("name") or payload.get("passenger_name") or "").strip()
    from_st = payload.get("from") or payload.get("from_station")
    to_st = payload.get("to") or payload.get("to_station")
    passengers = int(payload.get("passengers") or payload.get("count") or 1)
    email = payload.get("email", "")
    phone = payload.get("phone", "")
    payment = payload.get("payment") or payload.get("payment_method") or "UPI"

    if not name or not from_st or not to_st:
        raise HTTPException(status_code=400, detail="Name, departure and destination are required")

    d1 = STATIONS.get(from_st, 0)
    d2 = STATIONS.get(to_st, 0)
    distance = abs(d1 - d2)
    fare = float(payload.get("fare") or (distance * FARE_PER_KM * passengers))

    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%I:%M %p")
    qr_data = f"Name: {name}\nFrom: {from_st}\nTo: {to_st}\nPassengers: {passengers}\nFare: INR {fare:.2f}\nDate: {date_str}\nTime: {time_str}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tickets (passenger_name, from_station, to_station, distance_km, passengers, fare, payment_method, email, phone, ticket_date, ticket_time, qr_data, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, from_st, to_st, distance, passengers, fare, payment, email, phone, date_str, time_str, qr_data, now.isoformat()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "status": "success",
        "ticket_id": new_id,
        "name": name,
        "from": from_st,
        "to": to_st,
        "fare": fare,
        "date": date_str,
        "time": time_str,
        "qr_data": qr_data
    }

@router.get("/revenue-summary")
def get_revenue_summary():
    """Get total revenue and summary metrics from ticketing."""
    conn = get_db_connection()
    total_row = conn.execute("SELECT COUNT(*) as count, SUM(fare) as total_fare, SUM(passengers) as total_passengers FROM tickets").fetchone()
    conn.close()

    total_fare = total_row["total_fare"] or 0.0
    total_tickets = total_row["count"] or 0
    total_passengers = total_row["total_passengers"] or 0

    return {
        "total_revenue": round(total_fare, 2),
        "total_tickets": total_tickets,
        "total_passengers": total_passengers
    }
