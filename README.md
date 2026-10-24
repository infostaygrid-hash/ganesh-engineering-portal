# Ganesh Engineering Industries - Production & Inventory Logging Portal

**Project Type:** Industrial Training Project (Summer 2026)  
**Student:** Tushar (B.Tech CSE Core, 5th Semester)  
**Institution:** Lloyd Institute of Engineering & Technology, Greater Noida (AKTU)  
**Host Organisation:** Ganesh Engineering Industries, Rohtak, Haryana  
**Industry Supervisor:** Mr. Manish Saini (IT & Systems Lead)  

---

## 1. Project Overview
This web application was designed to replace paper-based job cards and physical shift logs with a centralized digital portal for tracking precision machined components and forging outputs across CNC/VMC cells.

### Core Modules:
1. **Production Dashboard (`/`):** Real-time summary cards displaying total machined parts, QA accepted parts, rejected parts, and calculated rejection rate (compliant with IATF 16949 standards).
2. **Shift Entry Form (`/add_log`):** Form for shift operators to log outputs by machine, shift (A/B/C), operator name, and QA defect reasons with built-in mathematical validation (`Total == Accepted + Rejected`).
3. **Component Master (`/components`):** Part directory registering engineering drawing numbers, component names, steel grades (EN8D, 20MnCr5, SAE 4140), and unit weights.
4. **CSV Export (`/export_csv`):** One-click download of all production logs formatted for shift handover and audit records.

---

## 2. Technology Stack
- **Backend:** Python 3.x, Flask
- **Database:** SQLite3 (`production.db`)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5, Bootstrap Icons
- **Server:** Local Intranet Server (Port 5000)

---

## 3. How to Run the Project

### Option A (Double Click):
Simply double-click the **`run.bat`** file in this directory. It will initialize the database and start the web server automatically.

### Option B (Terminal / Command Prompt):
```bash
# 1. Navigate to the project folder
cd D:\Internship_Project

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Seed database with sample parts and July 2026 shift logs
python seed_data.py

# 4. Run the web server
python app.py
```
Then open your browser and visit: **`http://127.0.0.1:5000`**

---

## 4. Viva Defense Cheat Sheet
- **Q: Why Flask and SQLite?**  
  *A:* "For a localized plant-floor intranet with 5–10 terminal workstations, Flask is lightweight with minimal server overhead, and SQLite requires zero maintenance or dedicated database servers."
- **Q: How does this prevent incorrect data entry?**  
  *A:* "We implemented client-side JavaScript checking plus server-side validation to ensure that `Accepted + Rejected == Total Produced`. Negative values are blocked at both levels."
- **Q: What is the defect taxonomy?**  
  *A:* "Rejections are tagged by specific industrial defects like Runout Error, Porosity/Blowhole, Thread Pitch Mismatch, or Tool Chatter Marks, making quality reporting under IATF 16949 instantaneous."
