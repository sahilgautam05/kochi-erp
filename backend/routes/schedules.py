from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/api/schedules", tags=["Schedule Management"])

def row_to_dict(r):
    d = dict(r)
    return {
        "id": d["id"],
        "trainId": d["train_id"],
        "train_id": d["train_id"],
        "route": d["route"],
        "departure": d["departure"],
        "arrival": d["arrival"],
        "driver": d["driver"],
        "status": d["status"]
    }

@router.get("", response_model=List[dict])
def list_schedules():
    """List all train schedules."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM schedules ORDER BY id ASC").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

@router.post("", status_code=201)
def add_schedule(schedule: dict):
    """Add a new train schedule."""
    train_id = schedule.get("trainId") or schedule.get("train_id")
    route = schedule.get("route", "")
    departure = schedule.get("departure", "")
    arrival = schedule.get("arrival", "")
    driver = schedule.get("driver", "")
    status = schedule.get("status", "Operational")

    if not train_id or not route:
        raise HTTPException(status_code=400, detail="Train ID and Route are required")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO schedules (train_id, route, departure, arrival, driver, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (train_id, route, departure, arrival, driver, status, datetime.now().isoformat()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"status": "success", "id": new_id, "message": f"Schedule for {train_id} saved successfully"}

@router.put("/{schedule_id}")
def update_schedule(schedule_id: int, schedule: dict):
    """Update an existing schedule."""
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM schedules WHERE id = ?", (schedule_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Schedule ID {schedule_id} not found")

    train_id = schedule.get("trainId") or schedule.get("train_id", existing["train_id"])
    route = schedule.get("route", existing["route"])
    departure = schedule.get("departure", existing["departure"])
    arrival = schedule.get("arrival", existing["arrival"])
    driver = schedule.get("driver", existing["driver"])
    status = schedule.get("status", existing["status"])

    conn.execute("""
    UPDATE schedules SET train_id = ?, route = ?, departure = ?, arrival = ?, driver = ?, status = ?
    WHERE id = ?
    """, (train_id, route, departure, arrival, driver, status, schedule_id))
    conn.commit()
    conn.close()

    return {"status": "success", "message": f"Schedule {schedule_id} updated successfully"}

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int):
    """Delete a schedule."""
    conn = get_db_connection()
    conn.execute("DELETE FROM schedules WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Schedule {schedule_id} deleted successfully"}
