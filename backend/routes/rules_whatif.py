from fastapi import APIRouter, Query
from typing import List, Optional
from database import get_db_connection

router = APIRouter(prefix="/api", tags=["Rules & What-If Analysis"])

@router.get("/rules")
def get_rules():
    """
    Returns train eligibility status and alerts for rules-based engine.
    Used by Status Chart and Alerts Distribution Chart.
    """
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, status, alerts, mileage, branding, stabling, score FROM train_rules").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/whatif/defaults")
def get_whatif_defaults():
    """
    Returns default weights and parameters for What-If optimization analysis.
    """
    return {
        "k": 10,
        "branding_weight": 0.5,
        "stabling_weight": 0.3
    }

@router.post("/whatif")
def calculate_whatif(
    k: int = Query(10, description="Number of top trains to evaluate"),
    branding_weight: float = Query(0.5, description="Branding weight factor"),
    stabling_weight: float = Query(0.3, description="Stabling weight factor")
):
    """
    Simulates What-If scenario optimization.
    Calculates dynamic scores based on mileage, branding, and stabling weights.
    Returns list of trains with both before (mileage) and after (score) metrics.
    """
    conn = get_db_connection()
    rows = conn.execute("SELECT id, name, status, alerts, mileage, branding, stabling, score FROM train_rules").fetchall()
    conn.close()

    results = []
    # Evaluate score dynamically
    for idx, row in enumerate(rows[:max(1, k)]):
        base_mileage = row["mileage"] or 50000
        # Normalization factor for mileage
        normalized_mileage_score = max(10.0, 100.0 - (base_mileage / 1500.0))
        
        # Branding factor (bonus for higher branding partnership)
        branding_factor = 20.0 if row["branding"] and row["branding"] != "None" else 5.0
        
        # Stabling factor (efficiency in depot/bay position)
        stabling_factor = 15.0 if "Bay" in (row["stabling"] or "") else 8.0
        
        # Optimization calculation
        calculated_score = round(
            (normalized_mileage_score * 0.5) +
            (branding_factor * float(branding_weight) * 2.0) +
            (stabling_factor * float(stabling_weight) * 2.0),
            2
        )
        
        results.append({
            "id": row["id"],
            "name": row["name"],
            "mileage": base_mileage,
            "score": calculated_score,
            "status": row["status"],
            "branding": row["branding"],
            "stabling": row["stabling"],
            "alerts": row["alerts"]
        })

    return results
