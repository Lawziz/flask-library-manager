# 📚 Library Management System

A modular, lightweight library management application built with **Flask**, **Flask-SQLAlchemy**, and **SQLite**. The system allows administrators to manage books and members, as well as handle real-time borrowing and returning mechanics with built-in relational database limits.

## 📁 Project Architecture

The application implements the **Flask Application Factory** design pattern to separate business logic, database configuration, and application routing cleanly:

project_folder/
│
├── run.py                 # Main entry point to run the Flask app
├── library.db             # Local SQLite database file (Auto-generated; ignored by Git)
├── .gitignore             # Tells Git to ignore tracking local DBs and environments
├── requirements.txt       # List of third-party library dependencies
├── README.md              # Technical project documentation overview
│
├── app/                   # core application package
│   ├── __init__.py        # App factory config (instantiates server instance)
│   ├── models.py          # Database structure schemas & relation hooks
│   ├── routes.py          # Server endpoint routes (processes incoming json requests)
│   │
│   ├── static/            # Static asset folder
│   │   ├── style.css      # Component stylesheet layouts
│   │   └── scripts.js     # AJAX API request scripts (handles user actions)
│   │
│   └── templates/         # HTML structure layer
│       └── index.html     # Client UI workspace view frame
│
└── tests/                 # Automated test engine
    └── test_app.py        # Isolated test cases (uses in-memory database)

---

## 🛠️ Features
* **Persistent Storage:** Powered by SQLite through Flask-SQLAlchemy (no volatile in-memory loss).
* **Automated Setup:** The application auto-generates tables and seeds sample data on its very first boot.
* **Relational Rules:** Built-in safeguards prevent deleting active members with unreturned books, borrowing already checked-out titles, or exceeding a **maximum borrow limit of 3 books**.

---

## 🚀 Getting Started

Follow these steps to set up and run the project on your work machine or personal computer.

### 1. Clone or Move to Your Project Directory
Open your terminal or command prompt and navigate to the project directory:
```bash
cd path/to/your_project
```

### 2. Set Up a Virtual Environment
Isolate your dependencies to avoid permissions conflicts (especially on work PCs):

**On Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Install Flask, Flask-SQLAlchemy, and runtime drivers via pip:
```bash
pip install flask-sqlalchemy blinker
```
*(Alternatively, create a `requirements.txt` containing those packages and run `pip install -r requirements.txt`)*

### 4. Run the Application
Execute the initialization entry script:
```bash
python run.py
```
The console will log that the local server is running at **`http://127.0.0.1:5000`**. Open that link in your browser to access the dashboard.

---

## 🔌 API Documentation Reference

The backend communicates strictly via JSON objects over the following REST endpoints:

### Core Data Delivery
* **`GET /api/data`** — Fetches full current inventory profiles for all books and members.

### Catalog Modifications
* **`POST /api/add_book`** — Registers a new title. Requires JSON: `{"title": "...", "author": "...", "isbn": "..."}`
* **`POST /api/add_member`** — Registers a new user. Requires JSON: `{"name": "...", "member_id": "..."}`
* **`POST /api/delete_book`** — Removes a title if it isn't currently borrowed. Requires JSON: `{"isbn": "..."}`
* **`POST /api/delete_member`** — Removes a member if they have zero outstanding books. Requires JSON: `{"member_id": "..."}`

### Circulation Operations
* **`POST /api/borrow`** — Lends an available book to a member. Requires JSON: `{"member_id": "...", "isbn": "..."}`
* **`POST /api/return`** — Checks back an outstanding book from a member. Requires JSON: `{"member_id": "...", "isbn": "..."}`
