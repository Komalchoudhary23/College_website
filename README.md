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

## 🐳 Quick Start with Docker (Recommended)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/isim-flask.git
cd isim-flask
```

### 2. Set up environment
```bash
cp .env.example .env
# Edit .env and change SECRET_KEY to something random
```

### 3. Start with Docker Compose
```bash
docker compose up --build
```

The app will be available at **http://localhost:5000**

Admin panel: **http://localhost:5000/admin**
- Username: `admin`
- Password: `admin123`

> **⚠️ Change the admin password immediately after first login!**

### Stop the app
```bash
docker compose down
# To also remove database data:
docker compose down -v
```

---

## 💻 Local Development (Without Docker)

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up MySQL locally
```sql
CREATE DATABASE isim_website;
CREATE USER 'isim_user'@'localhost' IDENTIFIED BY 'isim_password';
GRANT ALL PRIVILEGES ON isim_website.* TO 'isim_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env and set DATABASE_URL=mysql://isim_user:isim_password@localhost:3306/isim_website
```

### 5. Initialize database
```bash
export FLASK_APP=run.py
flask db init          # first time only
flask db migrate -m "initial tables"
flask db upgrade
flask seed             # creates admin user
```

### 6. Run the app
```bash
flask run
# or
python run.py
```

---

## 🌐 Deploy to Production (GitHub → Server)

### Option A: GitHub Actions + VPS

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/isim-flask
            git pull origin main
            docker compose up --build -d
```

Add secrets in GitHub: `Settings → Secrets → Actions`

### Option B: Deploy to Render.com (Free tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
5. Add a **MySQL** database in Render and copy the `DATABASE_URL`
6. Add environment variables in Render dashboard

### Option C: Railway.app

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add a MySQL plugin
4. Set environment variables (copy from `.env.example`)
5. Railway auto-detects Dockerfile and deploys

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

---

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | (required) |
| `MYSQL_HOST` | MySQL host | `db` |
| `MYSQL_DATABASE` | Database name | `isim_website` |
| `MYSQL_USER` | DB username | `isim_user` |
| `MYSQL_PASSWORD` | DB password | `isim_password` |
| `FLASK_ENV` | `development` or `production` | `development` |

---

## 🛠 Useful Commands

```bash
# View logs
docker compose logs -f web

# Open MySQL shell
docker compose exec db mysql -u isim_user -p isim_website

# Create a new migration after model changes
flask db migrate -m "describe change"
flask db upgrade

# Reset admin password
docker compose exec web flask seed
```
