# Binyad — Business, Management & IT Solutions Website

بنیاد — راه‌حل‌های مدیریت، اداری و تکنالوژی

Production-ready multilingual Django website for Binyad.

---

## Features

- Multilingual (Dari/Persian, Pashto, English) with automatic RTL/LTR
- Django Admin fully configured for all content
- Dynamic services, products, portfolio, blog, FAQ, testimonials, team
- Contact & consultation forms with admin tracking workflow
- SEO: per-page titles, descriptions, Open Graph, sitemap.xml, robots.txt
- WhatsApp contact (configurable via Site Settings)
- Security-first configuration (env vars, CSRF, secure cookies, upload limits)
- Fully responsive design with centralized theme variables

---

## Technology Stack

- Python 3.10+
- Django 5.x
- SQLite (dev) / PostgreSQL (prod)
- WhiteNoise, Gunicorn
- Pillow
- django-environ

---

## Local Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# edit .env with your values
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver