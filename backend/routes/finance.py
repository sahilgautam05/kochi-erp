from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/api/revenue", tags=["Finance & Revenue Department"])

@router.get("")
def list_revenue():
    """List all corporate sponsorship and non-fare revenue entries."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM revenue_entries ORDER BY id DESC").fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        results.append({
            "id": d["id"],
            "company": d["company"],
            "desc": d["description"],
            "description": d["description"],
            "rupees": d["rupees"],
            "ticketRupees": d["ticket_rupees"],
            "ticket_rupees": d["ticket_rupees"],
            "created_at": d["created_at"]
        })
    return results

@router.post("", status_code=201)
def add_revenue(entry: dict):
    """Add a new revenue entry from business partners/sponsors."""
    company = entry.get("company", "").strip()
    description = entry.get("desc") or entry.get("description", "").strip()
    rupees = float(entry.get("rupees") or 0.0)

    if not company or rupees <= 0:
        raise HTTPException(status_code=400, detail="Company name and valid revenue amount are required")

    conn = get_db_connection()
    # Get current ticket total
    ticket_row = conn.execute("SELECT SUM(fare) as total FROM tickets").fetchone()
    ticket_total = float(ticket_row["total"] or 0.0)

    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO revenue_entries (company, description, rupees, ticket_rupees, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (company, description, rupees, ticket_total, datetime.now().isoformat()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"status": "success", "id": new_id, "message": f"Revenue entry for {company} recorded successfully"}

@router.get("/summary")
def get_financial_summary():
    """Get complete financial summary combining fare and non-fare revenue."""
    conn = get_db_connection()
    corp_row = conn.execute("SELECT COUNT(*) as count, SUM(rupees) as total_corp FROM revenue_entries").fetchone()
    ticket_row = conn.execute("SELECT COUNT(*) as count, SUM(fare) as total_ticket FROM tickets").fetchone()
    conn.close()

    corp_rev = float(corp_row["total_corp"] or 0.0)
    ticket_rev = float(ticket_row["total_ticket"] or 0.0)

    return {
        "total_revenue": round(corp_rev + ticket_rev, 2),
        "corporate_sponsorship_revenue": round(corp_rev, 2),
        "ticketing_fare_revenue": round(ticket_rev, 2),
        "sponsorship_deals_count": corp_row["count"] or 0,
        "tickets_sold_count": ticket_row["count"] or 0
    }
