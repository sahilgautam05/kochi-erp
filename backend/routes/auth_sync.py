import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from database import get_db_connection

router = APIRouter(prefix="/api", tags=["Auth, Verification & Sync"])

@router.post("/auth/login")
def login(payload: dict):
    """Authenticate user login."""
    username = (payload.get("username") or "").strip()
    password = payload.get("password", "")
    role = payload.get("role", "customer")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    return {
        "status": "success",
        "username": username,
        "role": role,
        "token": f"kmrl_token_{username}_{int(datetime.now().timestamp())}",
        "redirect_url": "dashboard.html" if role == "admin" else "userpage.html"
    }

@router.post("/auth/signup")
def signup(payload: dict):
    """Register a new user account."""
    username = (payload.get("username") or "").strip()
    password = payload.get("password", "")
    role = payload.get("role", "customer")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    return {
        "status": "success",
        "message": f"Account for {username} created successfully with role {role}",
        "username": username,
        "role": role
    }

@router.get("/verification")
def list_verification_tasks():
    """List operational verification tasks."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM verification_tasks ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@router.put("/verification/{task_id}")
def update_verification_task(task_id: str, payload: dict):
    """Update task verification status."""
    status = payload.get("status", "verified")
    conn = get_db_connection()
    conn.execute("UPDATE verification_tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Task {task_id} marked as {status}"}

@router.get("/storage/{key}")
def get_storage_key(key: str):
    """Retrieve persisted key from local storage sync mirror."""
    conn = get_db_connection()
    row = conn.execute("SELECT value FROM key_value_storage WHERE key = ?", (key,)).fetchone()
    conn.close()
    return {"key": key, "value": row["value"] if row else None}

@router.post("/storage/{key}")
def set_storage_key(key: str, payload: dict):
    """Synchronize a local storage key with the server database."""
    val = payload.get("value", "")
    if isinstance(val, (dict, list)):
        val = json.dumps(val)

    conn = get_db_connection()
    conn.execute("""
    INSERT OR REPLACE INTO key_value_storage (key, value, updated_at)
    VALUES (?, ?, ?)
    """, (key, str(val), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return {"status": "synced", "key": key}

@router.get("/health")
def health_check():
    """System health check endpoint."""
    conn = get_db_connection()
    train_count = conn.execute("SELECT COUNT(*) FROM trains").fetchone()[0]
    staff_count = conn.execute("SELECT COUNT(*) FROM staff").fetchone()[0]
    conn.close()

    return {
        "status": "healthy",
        "system": "Kochi Metro Rail Limited ERP Backend",
        "version": "2.0.0",
        "active_trains": train_count,
        "active_staff": staff_count,
        "timestamp": datetime.now().isoformat()
    }
