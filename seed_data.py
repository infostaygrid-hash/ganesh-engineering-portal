import os
import sqlite3
import random

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = os.path.join(BASE_DIR, "production.db")

def seed():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Drop existing to reseed cleanly
    cursor.execute("DROP TABLE IF EXISTS components")
    cursor.execute("DROP TABLE IF EXISTS machines")
    cursor.execute("DROP TABLE IF EXISTS production_logs")

    cursor.execute('''CREATE TABLE components (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_number TEXT UNIQUE NOT NULL,
        part_name TEXT NOT NULL,
        material_grade TEXT NOT NULL,
        unit_weight_kg REAL NOT NULL
    )''')

    cursor.execute('''CREATE TABLE machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_code TEXT UNIQUE NOT NULL,
        machine_name TEXT NOT NULL,
        machine_type TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE production_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_date TEXT NOT NULL,
        shift TEXT NOT NULL,
        part_id INTEGER NOT NULL,
        machine_id TEXT NOT NULL,
        operator_name TEXT NOT NULL,
        total_produced INTEGER NOT NULL,
        accepted_qty INTEGER NOT NULL,
        rejected_qty INTEGER NOT NULL,
        rejection_reason TEXT,
        FOREIGN KEY (part_id) REFERENCES components(id)
    )''')

    # Seed Components typical of Ganesh Engineering Industries (Forging & Machining)
    sample_components = [
        ("GEI-FLG-101", "Precision Flange Shaft", "EN8D / Carbon Steel", 3.45),
        ("GEI-GB-204", "Spur Gear Blank", "20MnCr5 / Case Hardening Steel", 2.80),
        ("GEI-SPN-305", "Front Wheel Spindle Housing", "SAE 4140 / Alloy Steel", 5.20),
        ("GEI-YOK-412", "Forged Drive Flange Yoke", "C45 / Medium Carbon", 1.95),
        ("GEI-CRK-520", "Intermediate Connecting Bush", "Brass / Leaded Bronze", 0.85)
    ]
    cursor.executemany("INSERT INTO components (part_number, part_name, material_grade, unit_weight_kg) VALUES (?, ?, ?, ?)", sample_components)

    # Seed Machine Cells
    sample_machines = [
        ("CNC-01", "Doosan Puma 2600", "CNC Turning Center"),
        ("CNC-02", "Jyoti DX 200", "CNC Turning Center"),
        ("VMC-01", "BFW Chakra 400", "Vertical Machining Center"),
        ("LATHE-03", "HMT Heavy Duty", "Conventional Lathe"),
        ("GRIND-01", "Parishudh Precision", "Cylindrical Grinder")
    ]
    cursor.executemany("INSERT INTO machines (machine_code, machine_name, machine_type) VALUES (?, ?, ?)", sample_machines)

    # Seed 20+ realistic production logs across July 2026 (Internship duration: 01.07.2026 to 31.07.2026)
    operators = ["Ramesh Kumar", "Vikram Singh", "Sanjay Verma", "Amit Sharma", "Sunil Yadav"]
    shifts = ["Shift A (06:00 - 14:00)", "Shift B (14:00 - 22:00)", "Shift C (22:00 - 06:00)"]
    reasons = [
        "None (100% OK Batch)",
        "Dimensional Runout Error (+0.08mm)",
        "Surface Porosity / Blowhole (Forging Defect)",
        "Thread Pitch Mismatch",
        "Tool Chatter Marks (VMC Finish)"
    ]

    logs = []
    for day in range(1, 31):
        if day in [5, 12, 19, 26]:  # Skip Sundays
            continue
        date_str = f"2026-07-{day:02d}"
        for shift_idx in [0, 1]:  # 2 shifts per day
            part_id = random.randint(1, 5)
            machine = random.choice(["CNC-01", "CNC-02", "VMC-01", "GRIND-01"])
            operator = random.choice(operators)
            total = random.choice([120, 150, 180, 200, 220])
            rejected = random.choice([0, 1, 2, 3, 5, 8])
            accepted = total - rejected
            reason = "None (100% OK)" if rejected == 0 else random.choice(reasons[1:])
            
            logs.append((date_str, shifts[shift_idx], part_id, machine, operator, total, accepted, rejected, reason))

    cursor.executemany('''
        INSERT INTO production_logs 
        (log_date, shift, part_id, machine_id, operator_name, total_produced, accepted_qty, rejected_qty, rejection_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', logs)

    conn.commit()
    conn.close()
    print("Database seeded successfully with sample components, machines, and 50+ July 2026 shift logs!")

if __name__ == '__main__':
    seed()
