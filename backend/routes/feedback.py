from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/api/feedback", tags=["Customer Feedback"])

@router.get("")
def list_feedback():
    """List all passenger feedback submissions."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.post("", status_code=201)
def submit_feedback(payload: dict):
    """Submit passenger feedback."""
    name = (payload.get("name") or "").strip()
    email = payload.get("email", "").strip()
    phone = (payload.get("phone") or "").strip()
    from_st = payload.get("from") or payload.get("from_station", "")
    to_st = payload.get("to") or payload.get("to_station", "")
    journey_time = payload.get("journeyTime") or payload.get("journey_time", "")
    rating = int(payload.get("rating") or 5)
    comments = payload.get("comments", "").strip()

    if not name or not phone:
        raise HTTPException(status_code=400, detail="Name and Phone number are required")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO feedback (name, email, phone, from_station, to_station, journey_time, rating, comments, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, phone, from_st, to_st, journey_time, rating, comments, datetime.now().isoformat()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"status": "success", "id": new_id, "message": "Thank you for your feedback!"}

@router.get("/stats")
def feedback_stats():
    """Get average rating and satisfaction breakdown."""
    conn = get_db_connection()
    rows = conn.execute("SELECT rating, COUNT(*) as count FROM feedback GROUP BY rating").fetchall()
    avg_row = conn.execute("SELECT AVG(rating) as avg_rating, COUNT(*) as total FROM feedback").fetchone()
    conn.close()

    breakdown = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in rows:
        breakdown[r["rating"]] = r["count"]

    avg_rating = round(avg_row["avg_rating"] or 5.0, 1)
    total_count = avg_row["total"] or 0

    return {
        "average_rating": avg_rating,
        "total_reviews": total_count,
        "star_breakdown": breakdown
    }
