import sqlite3
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "metro_erp.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Trains Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trains (
        id TEXT PRIMARY KEY,
        name TEXT,
        route TEXT,
        driver TEXT,
        next_station TEXT,
        status TEXT,
        fitness TEXT,
        job_card TEXT,
        mileage INTEGER,
        cleaning_due TEXT,
        branding TEXT,
        bay_position TEXT,
        created_at TEXT
    )
    """)

    # 2. Staff Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        employee_id TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        status TEXT NOT NULL,
        image TEXT DEFAULT '',
        phone TEXT DEFAULT '',
        email TEXT DEFAULT '',
        created_at TEXT
    )
    """)

    # 3. Schedules Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_id TEXT NOT NULL,
        route TEXT NOT NULL,
        departure TEXT NOT NULL,
        arrival TEXT NOT NULL,
        driver TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT
    )
    """)

    # 4. Tickets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_name TEXT NOT NULL,
        from_station TEXT NOT NULL,
        to_station TEXT NOT NULL,
        distance_km REAL,
        passengers INTEGER DEFAULT 1,
        fare REAL NOT NULL,
        payment_method TEXT DEFAULT 'UPI',
        email TEXT DEFAULT '',
        phone TEXT DEFAULT '',
        ticket_date TEXT NOT NULL,
        ticket_time TEXT NOT NULL,
        qr_data TEXT,
        created_at TEXT
    )
    """)

    # 5. Feedback Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT NOT NULL,
        from_station TEXT NOT NULL,
        to_station TEXT NOT NULL,
        journey_time TEXT,
        rating INTEGER NOT NULL,
        comments TEXT,
        created_at TEXT
    )
    """)

    # 6. Revenue Entries Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revenue_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        description TEXT,
        rupees REAL NOT NULL,
        ticket_rupees REAL DEFAULT 0,
        created_at TEXT
    )
    """)

    # 7. Verification Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verification_tasks (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        details TEXT,
        status TEXT NOT NULL,
        inspector TEXT,
        created_at TEXT
    )
    """)

    # 8. Storage / Key-Value Sync Table (for frontend local storage mirror)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS key_value_storage (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at TEXT
    )
    """)

    # 9. Rules Table (for Rules / What-if optimization model)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS train_rules (
        id TEXT PRIMARY KEY,
        name TEXT,
        status TEXT,
        alerts TEXT,
        mileage INTEGER,
        branding TEXT,
        stabling TEXT,
        score REAL
    )
    """)

    conn.commit()

    # Seed initial data if tables are empty
    seed_initial_data(cursor, conn)
    conn.close()

def seed_initial_data(cursor, conn):
    # Seed Trains
    cursor.execute("SELECT COUNT(*) FROM trains")
    if cursor.fetchone()[0] == 0:
        initial_trains = [
            ("K101", "Kochi Express", "Aluva - Tripunithura", "Rajesh Kumar", "Edappally", "active", "Certified OK", "Completed", 54200, "2026-10-05", "Adani Group", "Bay 04", datetime.now().isoformat()),
            ("K102", "Periyar Voyager", "Tripunithura - Aluva", "Priya Nair", "Kakkanad", "delayed", "Certified OK", "Pending", 71340, "2026-09-30", "Lulu Group", "Track 2", datetime.now().isoformat()),
            ("K103", "Marine Drive Metro", "Aluva - Tripunithura", "Suresh Babu", "Kaloor", "active", "Certified OK", "Completed", 32100, "2026-10-12", "Muthoot Finance", "Bay 01", datetime.now().isoformat()),
            ("K104", "Depot Unit 04", "Maintenance Mode", "N/A", "Depot", "maintenance", "Under Inspection", "In Progress", 120500, "2026-09-28", "None", "Depot Bay 1", datetime.now().isoformat()),
            ("K105", "Queen of Arabian Sea", "Tripunithura - Aluva", "Meera Thomas", "Palarivattom", "active", "Certified OK", "Completed", 48900, "2026-10-02", "Federal Bank", "Bay 03", datetime.now().isoformat()),
            ("K106", "Vembanad Flyer", "Aluva - Tripunithura", "Ravi Menon", "M.G. Road", "active", "Certified OK", "Completed", 61200, "2026-10-08", "Aster DM", "Bay 02", datetime.now().isoformat())
        ]
        cursor.executemany("INSERT INTO trains VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", initial_trains)

    # Seed Staff
    cursor.execute("SELECT COUNT(*) FROM staff")
    if cursor.fetchone()[0] == 0:
        initial_staff = [
            ("Rajesh Kumar", "EMP001", "Train Driver", "On Duty", "", "+91 98470 12345", "rajesh.k@kochimetro.in", datetime.now().isoformat()),
            ("Priya Nair", "EMP002", "Train Driver", "On Duty", "", "+91 98470 23456", "priya.n@kochimetro.in", datetime.now().isoformat()),
            ("Suresh Babu", "EMP003", "Station Manager", "On Duty", "", "+91 98470 34567", "suresh.b@kochimetro.in", datetime.now().isoformat()),
            ("Arun Krishnan", "EMP004", "Maintenance Technician", "On Duty", "", "+91 98470 45678", "arun.k@kochimetro.in", datetime.now().isoformat()),
            ("Meera Thomas", "EMP005", "Train Driver", "On Duty", "", "+91 98470 56789", "meera.t@kochimetro.in", datetime.now().isoformat()),
            ("Ravi Menon", "EMP006", "Control Room Operator", "On Duty", "", "+91 98470 67890", "ravi.m@kochimetro.in", datetime.now().isoformat()),
            ("Ananya Pillai", "EMP007", "Customer Service", "On Duty", "", "+91 98470 78901", "ananya.p@kochimetro.in", datetime.now().isoformat()),
            ("Kavitha Varma", "EMP008", "Security Officer", "On Duty", "", "+91 98470 89012", "kavitha.v@kochimetro.in", datetime.now().isoformat())
        ]
        cursor.executemany("INSERT INTO staff (name, employee_id, department, status, image, phone, email, created_at) VALUES (?,?,?,?,?,?,?,?)", initial_staff)

    # Seed Schedules
    cursor.execute("SELECT COUNT(*) FROM schedules")
    if cursor.fetchone()[0] == 0:
        initial_schedules = [
            ("K101", "Aluva - Tripunithura", "06:00", "06:45", "Rajesh Kumar", "Operational", datetime.now().isoformat()),
            ("K102", "Tripunithura - Aluva", "06:30", "07:15", "Priya Nair", "Delayed", datetime.now().isoformat()),
            ("K103", "Aluva - Tripunithura", "07:00", "07:45", "Suresh Babu", "Operational", datetime.now().isoformat()),
            ("K104", "Maintenance Mode", "00:00", "00:00", "N/A", "Maintenance", datetime.now().isoformat()),
            ("K105", "Tripunithura - Aluva", "07:30", "08:15", "Meera Thomas", "Operational", datetime.now().isoformat()),
            ("K106", "Aluva - Tripunithura", "08:00", "08:45", "Ravi Menon", "Operational", datetime.now().isoformat())
        ]
        cursor.executemany("INSERT INTO schedules (train_id, route, departure, arrival, driver, status, created_at) VALUES (?,?,?,?,?,?,?)", initial_schedules)

    # Seed Verification Tasks
    cursor.execute("SELECT COUNT(*) FROM verification_tasks")
    if cursor.fetchone()[0] == 0:
        initial_tasks = [
            ("K101", "Morning Operations - K101", "Route: Aluva - Tripunithura<br>Driver: Rajesh Kumar", "pending", "Rajesh Kumar", datetime.now().isoformat()),
            ("K103", "Safety Inspection - K103", "Type: Weekly Safety Check<br>Inspector: Suresh Babu", "pending", "Suresh Babu", datetime.now().isoformat()),
            ("K102", "Evening Operations - K102", "Route: Tripunithura - Aluva<br>Driver: Priya Nair", "verified", "Priya Nair", datetime.now().isoformat()),
            ("K104", "Maintenance Check - K104", "Type: Routine Maintenance<br>Technician: Arun Krishnan", "in-progress", "Arun Krishnan", datetime.now().isoformat()),
            ("L1", "Route Inspection - Line 1", "Section: Aluva to Edappally<br>Inspector: Meera Thomas", "verified", "Meera Thomas", datetime.now().isoformat()),
            ("S5", "Emergency Drill - Station 5", "Location: Ernakulam South<br>Coordinator: Ravi Menon", "pending", "Ravi Menon", datetime.now().isoformat())
        ]
        cursor.executemany("INSERT INTO verification_tasks VALUES (?,?,?,?,?,?)", initial_tasks)

    # Seed Rules Data
    cursor.execute("SELECT COUNT(*) FROM train_rules")
    if cursor.fetchone()[0] == 0:
        initial_rules = [
            ("K101", "Kochi Express", "Eligible", "-", 54200, "Adani Group", "Bay 04", 88.5),
            ("K102", "Periyar Voyager", "Eligible", "Minor Delay Alert", 71340, "Lulu Group", "Track 2", 76.2),
            ("K103", "Marine Drive Metro", "Eligible", "-", 32100, "Muthoot Finance", "Bay 01", 94.0),
            ("K104", "Depot Unit 04", "Blocked", "Critical Overdue, Brake Wear", 120500, "None", "Depot Bay 1", 35.0),
            ("K105", "Queen of Arabian Sea", "Eligible", "-", 48900, "Federal Bank", "Bay 03", 91.5),
            ("K106", "Vembanad Flyer", "Eligible", "Cleaning Pending", 61200, "Aster DM", "Bay 02", 82.0),
            ("K107", "Backwater Cruiser", "Blocked", "HVAC Malfunction", 98000, "None", "Depot Bay 2", 42.0),
            ("K108", "Cochin Pride", "Eligible", "-", 29500, "Joyalukkas", "Bay 05", 96.0)
        ]
        cursor.executemany("INSERT INTO train_rules VALUES (?,?,?,?,?,?,?,?)", initial_rules)

    # Seed Revenue
    cursor.execute("SELECT COUNT(*) FROM revenue_entries")
    if cursor.fetchone()[0] == 0:
        initial_revenue = [
            ("Lulu International Shopping Mall", "Station Naming & Media Rights", 450000.0, 185000.0, datetime.now().isoformat()),
            ("Muthoot Finance Ltd", "Train Wrap & Digital Displays", 320000.0, 185000.0, datetime.now().isoformat()),
            ("Federal Bank", "Automated Fare Collection Kiosk Sponsorship", 280000.0, 185000.0, datetime.now().isoformat())
        ]
        cursor.executemany("INSERT INTO revenue_entries (company, description, rupees, ticket_rupees, created_at) VALUES (?,?,?,?,?)", initial_revenue)

    # Seed Sample Tickets
    cursor.execute("SELECT COUNT(*) FROM tickets")
    if cursor.fetchone()[0] == 0:
        initial_tickets = [
            ("John Doe", "Aluva", "Maharajas", 14.0, 1, 56.0, "UPI", "john@example.com", "9876543210", datetime.now().strftime("%d/%m/%Y"), "08:30 AM", "Sample QR Data", datetime.now().isoformat()),
            ("Aisha Rahman", "Edapally", "Vyttila", 4.0, 2, 32.0, "Credit/Debit Card", "aisha@example.com", "9876543211", datetime.now().strftime("%d/%m/%Y"), "09:15 AM", "Sample QR Data", datetime.now().isoformat())
        ]
        cursor.executemany("INSERT INTO tickets (passenger_name, from_station, to_station, distance_km, passengers, fare, payment_method, email, phone, ticket_date, ticket_time, qr_data, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", initial_tickets)

    conn.commit()

init_db()
