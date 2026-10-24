# =====================================================================
# PROJECT: Production & Inventory Logging Portal
# ORGANISATION: Ganesh Engineering Industries, Rohtak
# STUDENT NAME: Tushar (B.Tech CSE Core - 5th Semester)
# COLLEGE: Lloyd Institute of Engineering & Technology, Greater Noida
# SUPERVISOR: Mr. Manish Saini (IT & Systems Lead)
# =====================================================================

import os
import sqlite3
import csv
import io
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash, Response

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "ganesh_engineering_secret_key_2026"

ORIGINAL_DB = os.path.join(BASE_DIR, "production.db")

# Setup database path (handles writable /tmp directory if running on Vercel)
if os.environ.get("VERCEL"):
    TMP_DB = "/tmp/production.db"
    if not os.path.exists(TMP_DB):
        if os.path.exists(ORIGINAL_DB):
            shutil.copyfile(ORIGINAL_DB, TMP_DB)
        else:
            # Create fresh if not bundled
            pass
    DB_NAME = TMP_DB
else:
    DB_NAME = ORIGINAL_DB

# Helper function to connect to SQLite database
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create tables if they don't exist
def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT UNIQUE NOT NULL,
            part_name TEXT NOT NULL,
            material_grade TEXT NOT NULL,
            unit_weight_kg REAL NOT NULL
        )''')

        conn.execute('''CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_code TEXT UNIQUE NOT NULL,
            machine_name TEXT NOT NULL,
            machine_type TEXT NOT NULL
        )''')

        conn.execute('''CREATE TABLE IF NOT EXISTS production_logs (
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
        conn.commit()

# Ensure DB is initialized on cold-start
try:
    init_db()
except Exception:
    pass

# Route 1: Home page / Dashboard showing shift logs and total numbers
@app.route('/')
def index():
    conn = get_db()
    
    # Calculate total stats for the top summary cards
    stats = conn.execute('''
        SELECT 
            COALESCE(SUM(total_produced), 0) as total_prod,
            COALESCE(SUM(accepted_qty), 0) as total_accepted,
            COALESCE(SUM(rejected_qty), 0) as total_rejected
        FROM production_logs
    ''').fetchone()

    total_prod = stats['total_prod']
    total_accepted = stats['total_accepted']
    total_rejected = stats['total_rejected']
    rejection_rate = round((total_rejected / total_prod * 100), 2) if total_prod > 0 else 0

    # Fetch all production logs joined with component table
    logs = conn.execute('''
        SELECT l.*, c.part_number, c.part_name 
        FROM production_logs l 
        JOIN components c ON l.part_id = c.id 
        ORDER BY l.log_date DESC, l.id DESC
    ''').fetchall()

    return render_template('index.html', 
                           logs=logs, 
                           total_prod=total_prod, 
                           total_accepted=total_accepted, 
                           total_rejected=total_rejected, 
                           rejection_rate=rejection_rate)

# Route 2: Form to add a new shift production entry
@app.route('/add_log', methods=['GET', 'POST'])
def add_log():
    conn = get_db()
    if request.method == 'POST':
        log_date = request.form['log_date']
        shift = request.form['shift']
        part_id = request.form['part_id']
        machine_id = request.form['machine_id']
        operator_name = request.form['operator_name']
        total_produced = int(request.form['total_produced'])
        accepted_qty = int(request.form['accepted_qty'])
        rejected_qty = int(request.form['rejected_qty'])
        rejection_reason = request.form.get('rejection_reason', 'None')

        # Validation: check if sum matches total
        if accepted_qty + rejected_qty != total_produced:
            flash("Error: Accepted + Rejected quantity must equal Total Produced!", "danger")
            return redirect(url_for('add_log'))

        # Insert record into database
        conn.execute('''
            INSERT INTO production_logs 
            (log_date, shift, part_id, machine_id, operator_name, total_produced, accepted_qty, rejected_qty, rejection_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (log_date, shift, part_id, machine_id, operator_name, total_produced, accepted_qty, rejected_qty, rejection_reason))
        conn.commit()
        flash("Shift entry saved successfully in database!", "success")
        return redirect(url_for('index'))

    # Load parts and machines for the dropdowns
    components = conn.execute('SELECT * FROM components ORDER BY part_name ASC').fetchall()
    machines = conn.execute('SELECT * FROM machines ORDER BY machine_code ASC').fetchall()
    return render_template('add_log.html', components=components, machines=machines)

# Route 3: View and add new parts in Master directory
@app.route('/components', methods=['GET', 'POST'])
def components():
    conn = get_db()
    if request.method == 'POST':
        part_number = request.form['part_number'].strip().upper()
        part_name = request.form['part_name'].strip()
        material_grade = request.form['material_grade'].strip()
        unit_weight_kg = float(request.form['unit_weight_kg'])

        try:
            conn.execute('''
                INSERT INTO components (part_number, part_name, material_grade, unit_weight_kg)
                VALUES (?, ?, ?, ?)
            ''', (part_number, part_name, material_grade, unit_weight_kg))
            conn.commit()
            flash(f"New part '{part_name}' added successfully!", "success")
        except sqlite3.IntegrityError:
            flash(f"Warning: Part Number '{part_number}' already exists in database!", "danger")

        return redirect(url_for('components'))

    comp_list = conn.execute('SELECT * FROM components ORDER BY id DESC').fetchall()
    return render_template('components.html', components=comp_list)

# Route 4: Export records to CSV file for supervisor report
@app.route('/export_csv')
def export_csv():
    conn = get_db()
    logs = conn.execute('''
        SELECT l.id, l.log_date, l.shift, c.part_number, c.part_name, l.machine_id, 
               l.operator_name, l.total_produced, l.accepted_qty, l.rejected_qty, l.rejection_reason
        FROM production_logs l
        JOIN components c ON l.part_id = c.id
        ORDER BY l.log_date DESC
    ''').fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Date', 'Shift', 'Part No', 'Part Name', 'Machine', 'Operator', 'Total Produced', 'Accepted Qty', 'Rejected Qty', 'Reason'])
    
    for row in logs:
        writer.writerow(list(row))
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=shift_production_records.csv"}
    )

if __name__ == '__main__':
    init_db()
    print("Running Flask server on http://127.0.0.1:5000 ...")
    app.run(debug=True, host='127.0.0.1', port=5000)
