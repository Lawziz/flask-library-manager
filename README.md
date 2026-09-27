# Flask Library Manager

A small library-management web app built with Flask. It provides a dashboard for tracking books and members, registering new records, and borrowing or returning books.

## Features

- View the book inventory and registered members
- Add books and members
- Borrow and return books
- Limit each member to three borrowed books
- Reject duplicate ISBNs and member IDs

## Requirements

- Python 3.10 or newer

## Run Locally

In PowerShell, from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Data and Development

The app stores data in memory, so books and members added while it is running are reset when the server restarts. The included books and members are sample records initialized by the app. `app.py` starts Flask in debug mode for local development; use a production WSGI server before deploying publicly.