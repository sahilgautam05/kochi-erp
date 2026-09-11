import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from database import get_db_connection

router = APIRouter(prefix="/api", tags=["Auth, Verification & Sync"])

@router.post("/auth/login")
def login(payload: dict):
    """Authenticate user login with strict database verification."""
    username = (payload.get("username") or "").strip()
    password = payload.get("password", "")
    role = (payload.get("role") or "customer").strip().lower()

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?", 
        (username.lower(), username.lower())
    ).fetchone()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User '{username}' does not exist in the database. Please register first."
        )

    user_dict = dict(user)
    if user_dict["password"] != password:
        raise HTTPException(
            status_code=401, 
            detail="Incorrect password! Please check your credentials and try again."
        )

    user_dict.pop("password", None)
    actual_role = user_dict.get("role", "customer")
    
    return {
        "status": "success",
        "message": "Authentication successful",
        "user": user_dict,
        "username": user_dict["username"],
        "role": actual_role,
        "token": f"kmrl_token_{user_dict['username']}_{int(datetime.now().timestamp())}",
        "redirect_url": "dashboard.html" if actual_role == "admin" else "userpage.html"
    }

@router.post("/auth/signup")
def signup(payload: dict):
    """Register a new user account in database."""
    username = (payload.get("username") or "").strip()
    password = payload.get("password", "")
    email = (payload.get("email") or "").strip()
    full_name = (payload.get("full_name") or payload.get("name") or username).strip()
    role = (payload.get("role") or "customer").strip().lower()
    department = payload.get("department", "Operations Management" if role == "admin" else "Passenger Services")
    designation = payload.get("designation", "System Administrator" if role == "admin" else "Commuter")
    phone = payload.get("phone", "+91 98470 12345")
    avatar = payload.get("avatar", "https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=96&h=96&fit=crop&crop=face" if role == "admin" else "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=96&h=96&fit=crop&crop=face")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")
    if not email:
        email = f"{username}@kochimetro.org"

    conn = get_db_connection()
    existing = conn.execute(
        "SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?", 
        (username.lower(), email.lower())
    ).fetchone()
    if existing:
        conn.close()
        raise HTTPException(
            status_code=409, 
            detail=f"User with username '{username}' or email '{email}' already exists in database."
        )

    now = datetime.now().isoformat()
    conn.execute("""
    INSERT INTO users (username, password, email, full_name, role, department, designation, phone, avatar, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, password, email, full_name, role, department, designation, phone, avatar, now))
    conn.commit()

    created_user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()

    user_dict = dict(created_user)
    user_dict.pop("password", None)

    return {
        "status": "success",
        "message": f"Account for {username} created successfully with role {role}",
        "user": user_dict,
        "username": username,
        "role": role,
        "token": f"kmrl_token_{username}_{int(datetime.now().timestamp())}",
        "redirect_url": "dashboard.html" if role == "admin" else "userpage.html"
    }

@router.get("/auth/user/{username}")
def get_user_profile(username: str):
    """Retrieve user profile from database."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id, username, email, full_name, role, department, designation, phone, avatar, created_at FROM users WHERE LOWER(username) = ?",
        (username.lower(),)
    ).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    return dict(user)

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
