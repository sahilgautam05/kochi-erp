from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from database import get_db_connection

router = APIRouter(prefix="/api/trains", tags=["Train Operations"])

class TrainModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = ""
    route: Optional[str] = ""
    driver: Optional[str] = ""
    next: Optional[str] = Field(default="", alias="next_station")
    status: Optional[str] = "active"
    fitness: Optional[str] = "Certified OK"
    jobCard: Optional[str] = Field(default="Completed", alias="job_card")
    mileage: Optional[int] = 0
    cleaningDue: Optional[str] = Field(default="", alias="cleaning_due")
    branding: Optional[str] = "None"
    bayPosition: Optional[str] = Field(default="Bay 01", alias="bay_position")

    class Config:
        populate_by_name = True

def row_to_dict(row):
    d = dict(row)
    # Ensure frontend property names are mapped
    return {
        "id": d["id"],
        "name": d["name"],
        "route": d["route"],
        "driver": d["driver"],
        "next": d["next_station"],
        "next_station": d["next_station"],
        "status": d["status"],
        "fitness": d["fitness"],
        "jobCard": d["job_card"],
        "job_card": d["job_card"],
        "mileage": d["mileage"],
        "cleaningDue": d["cleaning_due"],
        "cleaning_due": d["cleaning_due"],
        "branding": d["branding"],
        "bayPosition": d["bay_position"],
        "bay_position": d["bay_position"]
    }

@router.get("", response_model=List[dict])
def list_trains():
    """Get all registered trains."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM trains ORDER BY id ASC").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

@router.get("/{train_id}")
def get_train(train_id: str):
    """Get a single train by its ID."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM trains WHERE id = ?", (train_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Train {train_id} not found")
    return row_to_dict(row)

@router.post("", status_code=201)
def create_train(train: dict):
    """Add a new train to operations."""
    train_id = train.get("id") or f"K{abs(hash(train.get('name', '')) % 900) + 100}"
    name = train.get("name", "")
    route = train.get("route", "")
    driver = train.get("driver", "")
    next_station = train.get("next") or train.get("next_station", "")
    status = train.get("status", "active")
    fitness = train.get("fitness", "Certified OK")
    job_card = train.get("jobCard") or train.get("job_card", "Completed")
    mileage = int(train.get("mileage") or 0)
    cleaning_due = train.get("cleaningDue") or train.get("cleaning_due", "")
    branding = train.get("branding", "None")
    bay_position = train.get("bayPosition") or train.get("bay_position", "Bay 01")

    conn = get_db_connection()
    try:
        conn.execute("""
        INSERT OR REPLACE INTO trains (id, name, route, driver, next_station, status, fitness, job_card, mileage, cleaning_due, branding, bay_position, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (train_id, name, route, driver, next_station, status, fitness, job_card, mileage, cleaning_due, branding, bay_position, datetime.now().isoformat()))
        conn.commit()
    finally:
        conn.close()

    return {"status": "success", "message": f"Train {train_id} added successfully", "id": train_id}

@router.put("/{train_id}")
def update_train(train_id: str, train: dict):
    """Update train operations details."""
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM trains WHERE id = ?", (train_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Train {train_id} not found")

    name = train.get("name", existing["name"])
    route = train.get("route", existing["route"])
    driver = train.get("driver", existing["driver"])
    next_station = train.get("next") or train.get("next_station", existing["next_station"])
    status = train.get("status", existing["status"])
    fitness = train.get("fitness", existing["fitness"])
    job_card = train.get("jobCard") or train.get("job_card", existing["job_card"])
    mileage = int(train.get("mileage", existing["mileage"]) or 0)
    cleaning_due = train.get("cleaningDue") or train.get("cleaning_due", existing["cleaning_due"])
    branding = train.get("branding", existing["branding"])
    bay_position = train.get("bayPosition") or train.get("bay_position", existing["bay_position"])

    conn.execute("""
    UPDATE trains SET name=?, route=?, driver=?, next_station=?, status=?, fitness=?, job_card=?, mileage=?, cleaning_due=?, branding=?, bay_position=?
    WHERE id=?
    """, (name, route, driver, next_station, status, fitness, job_card, mileage, cleaning_due, branding, bay_position, train_id))
    conn.commit()
    conn.close()

    return {"status": "success", "message": f"Train {train_id} updated successfully"}

@router.delete("/{train_id}")
def delete_train(train_id: str):
    """Remove a train from operations."""
    conn = get_db_connection()
    conn.execute("DELETE FROM trains WHERE id = ?", (train_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Train {train_id} deleted successfully"}
