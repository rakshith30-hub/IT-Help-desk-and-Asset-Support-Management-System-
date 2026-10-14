import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-development-key")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "IT_Helpdesk"),
    "connection_timeout": 5,
}
DB_PORTS = [int(os.getenv("DB_PORT", "3306")), 3307, 3306]


def get_connection():
    last_error = None
    tried = set()
    for port in DB_PORTS:
        if port in tried:
            continue
        tried.add(port)
        try:
            config = dict(DB_CONFIG)
            config["port"] = port
            return mysql.connector.connect(**config)
        except Error as exc:
            last_error = exc
    raise last_error or RuntimeError("Could not connect to MySQL.")


def fetch_all(query, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params or ())
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()


def get_ticket_report():
    return fetch_all("SELECT * FROM Ticket_Report ORDER BY ticket_id DESC")


@app.route("/")
def index():
    try:
        tickets = get_ticket_report()
        total = len(tickets)
        open_count = sum(1 for t in tickets if str(t.get("status", "")).lower() in ("open", "new", "pending"))
        high_count = sum(1 for t in tickets if str(t.get("priority", "")).lower() in ("high", "critical", "urgent"))
        recent = tickets[:5]
        return render_template("index.html", tickets=recent, total=total,
                               open_count=open_count, high_count=high_count, db_error=None)
    except Exception as exc:
        return render_template("index.html", tickets=[], total=0, open_count=0,
                               high_count=0, db_error=str(exc))


@app.route("/tickets")
def tickets():
    try:
        all_tickets = get_ticket_report()
        return render_template("tickets.html", tickets=all_tickets, db_error=None)
    except Exception as exc:
        return render_template("tickets.html", tickets=[], db_error=str(exc))


@app.route("/new-ticket", methods=["GET", "POST"])
def new_ticket():
    try:
        users = fetch_all("SELECT user_id, user_name FROM Users ORDER BY user_name")
        technicians = fetch_all("SELECT technician_id, technician_name FROM Technicians ORDER BY technician_name")
        assets = fetch_all("SELECT asset_id, asset_name FROM Assets ORDER BY asset_name")
    except Exception as exc:
        flash(f"Could not load dropdowns from MySQL: {exc}", "error")
        users, technicians, assets = [], [], []

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        status = request.form.get("status", "Open")
        user_id = request.form.get("user_id") or None
        technician_id = request.form.get("technician_id") or None
        asset_id = request.form.get("asset_id") or None

        if not title or not description or not user_id:
            flash("Please enter a title, description, and select a requester.", "error")
            return render_template("new_ticket.html", users=users, technicians=technicians, assets=assets)

        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Expected schema: Tickets(title, description, priority, status, user_id,
            # technician_id, asset_id, created_at). Adjust if your table differs.
            cur.execute(
                """INSERT INTO Tickets
                   (title, description, priority, status, user_id, technician_id, asset_id, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (title, description, priority, status, int(user_id),
                 int(technician_id) if technician_id else None,
                 int(asset_id) if asset_id else None, datetime.now())
            )
            conn.commit()
            flash("Ticket created successfully!", "success")
            return redirect(url_for("tickets"))
        except Exception as exc:
            if conn:
                conn.rollback()
            flash(f"Could not create ticket. Check your Tickets table columns. Details: {exc}", "error")
        finally:
            if cur:
                cur.close()
            if conn and conn.is_connected():
                conn.close()

    return render_template("new_ticket.html", users=users, technicians=technicians, assets=assets)


@app.route("/health")
def health():
    try:
        conn = get_connection()
        port = conn.get_server_info()
        conn.close()
        return {"status": "connected", "mysql_server_version": port}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}, 500


if __name__ == "__main__":
    app.run(debug=True)
