# ISIM Website — Flask + MySQL + Docker

A full-featured college website for **ISIM (Institute of Management)** converted from PHP to Python Flask. Includes a public-facing website and an admin panel with full CRUD operations.

## 🚀 Features

**Public Website:**
- Home page with hero, stats, programs & latest news
- About, Vision & Mission pages
- MBA / MCA / PhD program pages
- Faculty directory
- News & Activities with category filtering and pagination
- Admission request form
- Contact form
- Placement page

**Admin Panel (`/admin`):**
- Secure login with hashed passwords
- Dashboard with stats & recent admissions
- Manage Admission Requests
- Manage News (with image & PDF upload)
- Manage Teachers
- Manage Lectures
- View Contact Messages
- Change Password

---



## 📁 Project Structure

```
isim-flask/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/
│   │   └── __init__.py      # SQLAlchemy models
│   ├── routes/
│   │   ├── public.py        # Public website routes
│   │   └── admin.py         # Admin panel routes
│   ├── static/
│   │   └── uploads/         # User-uploaded files
│   └── templates/
│       ├── public/          # Public page templates
│       └── admin/           # Admin panel templates
├── migrations/              # Flask-Migrate database migrations
├── config.py                # App configuration
├── run.py                   # Entry point + CLI commands
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── .env.example
└── .gitignore
```

