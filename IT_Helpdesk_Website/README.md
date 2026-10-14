# IT Helpdesk & Asset Support Management System

A starter Flask website for the DBMS project. It connects to the local MySQL database `IT_Helpdesk` and displays the `Ticket_Report` view.

## 1. Requirements
- Python 3.10 or newer
- MySQL Server running
- Your `IT_Helpdesk` database and `Ticket_Report` view created in MySQL Workbench

## 2. Open in VS Code
1. Extract the ZIP file.
2. In VS Code, select **File → Open Folder** and open `IT_Helpdesk_Website`.
3. Open **Terminal → New Terminal**.

## 3. Install packages
Windows:
```powershell
py -m pip install -r requirements.txt
```
If `py` is not recognized, try:
```powershell
python -m pip install -r requirements.txt
```

## 4. Configure MySQL
Open `app.py` and check the database settings near the top:
```python
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "IT_Helpdesk"),
    "connection_timeout": 5,
}
```
Set your actual MySQL username and password. The app tries the port specified by `DB_PORT` (3306 by default), then 3307 and 3306.

PowerShell example for the current terminal only:
```powershell
$env:DB_USER="root"
$env:DB_PASSWORD="YOUR_MYSQL_PASSWORD"
$env:DB_PORT="3306"
```
If you have no password, leave `DB_PASSWORD` unset or set it to an empty string.

## 5. Run website
```powershell
py app.py
```
Open the local address printed in the terminal, usually `http://127.0.0.1:5000`.

## Pages
- `/` — dashboard and ticket counts
- `/tickets` — ticket report
- `/new-ticket` — form to insert a ticket
- `/health` — checks whether the app can connect to MySQL

## Database assumptions
The dashboard and tickets page need a MySQL view named `Ticket_Report`, based on the project SQL script.
The new-ticket form expects the `Tickets` table to have these columns:
`title, description, priority, status, user_id, technician_id, asset_id, created_at`.
It also expects these lookup columns:
- `Users(user_id, user_name)`
- `Technicians(technician_id, technician_name)`
- `Assets(asset_id, asset_name)`

If your actual table uses different column names, the ticket creation form may need a small adjustment. Do not share your database password or commit it to a public repository.
