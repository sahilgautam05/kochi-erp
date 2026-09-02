from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(prefix="/api/staff", tags=["Staff Management"])

def row_to_dict(r):
    d = dict(r)
    return {
        "id": d["id"],
        "name": d["name"],
        "employeeId": d["employee_id"],
        "employee_id": d["employee_id"],
        "department": d["department"],
        "status": d["status"],
        "phone": d.get("phone", ""),
        "email": d.get("email", ""),
        "image": d.get("image", "")
    }

@router.get("", response_model=List[dict])
def list_staff():
    """List all staff members."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM staff ORDER BY id ASC").fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]

@router.get("/{employee_id}")
def get_staff_member(employee_id: str):
    """Get staff member details by employee ID."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM staff WHERE employee_id = ?", (employee_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Staff with ID {employee_id} not found")
    return row_to_dict(row)

@router.post("", status_code=201)
def add_staff(staff: dict):
    """Add a new staff member."""
    name = staff.get("name", "").strip()
    employee_id = (staff.get("employeeId") or staff.get("employee_id") or "").strip()
    department = staff.get("department", "Station Staff")
    status = staff.get("status", "On Duty")
    phone = staff.get("phone", "")
    email = staff.get("email", "")
    image = staff.get("image", "")

    if not name or not employee_id:
        raise HTTPException(status_code=400, detail="Name and Employee ID are required")

    conn = get_db_connection()
    try:
        conn.execute("""
        INSERT INTO staff (name, employee_id, department, status, phone, email, image, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, employee_id, department, status, phone, email, image, datetime.now().isoformat()))
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Could not add staff member: {str(e)}")

    conn.close()
    return {"status": "success", "message": f"Staff member {name} ({employee_id}) added successfully"}

@router.put("/{employee_id}")
def update_staff(employee_id: str, staff: dict):
    """Update staff details / status."""
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM staff WHERE employee_id = ?", (employee_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Staff with ID {employee_id} not found")

    name = staff.get("name", existing["name"])
    department = staff.get("department", existing["department"])
    status = staff.get("status", existing["status"])
    phone = staff.get("phone", existing["phone"])
    email = staff.get("email", existing["email"])

    conn.execute("""
    UPDATE staff SET name = ?, department = ?, status = ?, phone = ?, email = ?
    WHERE employee_id = ?
    """, (name, department, status, phone, email, employee_id))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Staff {employee_id} updated successfully"}

@router.delete("/{employee_id}")
def delete_staff(employee_id: str):
    """Delete a staff member."""
    conn = get_db_connection()
    conn.execute("DELETE FROM staff WHERE employee_id = ?", (employee_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"Staff {employee_id} deleted successfully"}
