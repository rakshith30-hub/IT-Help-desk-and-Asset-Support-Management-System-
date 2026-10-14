# IT Helpdesk and Asset Support Management System

A database-backed web application for managing IT complaints, technicians
and IT assets in an organisation. Built as a Database Management Systems
(DBMS) Project-Based Learning (PBL) project at Woxsen University, Hyderabad.

## Presentation
The project presentation is included in this repository:

**[IT_Helpdesk_DBMS_PBL_Presentation.pptx](docs/IT_Helpdesk_DBMS_PBL_Presentation.pptx)**
(click the file on GitHub, then **Download raw file** to open it in PowerPoint)

The 14 slides cover the problem, objectives, technologies, architecture,
database design and ER diagram, SQL implementation, normalization, the Flask
website, the testing plan, and the conclusion.

## Overview
Manual complaint handling (calls, chats, spreadsheets) leads to duplicate
data, lost tickets and no history. This project replaces it with a
relational MySQL database (`IT_Helpdesk`) and a Flask website where
employees can report issues and support staff can track them.

## Features
- Dashboard with ticket counts and recent tickets
- Tickets page listing ticket records
- Create-ticket form (title, description, requester, technician,
  asset, priority, status)
- Ticket status history and a `Ticket_Report` view for reporting
- SQL examples: joins, GROUP BY / HAVING, views

## Database design
Six tables connected by one-to-many relationships:

| Table | Purpose |
|---|---|
| Departments | Organisation departments |
| Users | Employees who raise tickets |
| Technicians | Support staff |
| Assets | IT assets with purchase and warranty details |
| Tickets | Complaints with priority and status |
| Ticket_History | Status changes of each ticket |

## Tech stack
MySQL, MySQL Workbench, Python, Flask, MySQL Connector/Python,
HTML, CSS, Visual Studio Code

## Project structure
```
app.py
requirements.txt
templates/   base.html, index.html, tickets.html, new_ticket.html
static/      style.css
docs/        IT_Helpdesk_DBMS_PBL_Presentation.pptx
IT_Helpdesk_Project.sql
```

## Setup
1. Install Python 3 and MySQL.
2. Run `IT_Helpdesk_Project.sql` in MySQL Workbench to create the database.
3. Install dependencies: `pip install -r requirements.txt`
4. Set your database credentials (host, user, password) in a local `.env`
   file or environment variables. Do not commit this file.
5. Start the app: `python app.py`
6. Open http://127.0.0.1:5000

## Status and limitations
- Academic prototype; not a production system.
- No login or role-based access yet.
- Test results are still being recorded.

## Future work
Login and roles, technician reassignment, automatic ticket history,
search and filters, warranty reminders, email notifications, charts.

## Author
Rakshit Vivek Chanmanwar (25WU0102223), B.Tech AI & ML
Faculty: Dr. C Nagaraju
Woxsen University, Hyderabad
