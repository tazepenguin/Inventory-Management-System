# Inventory Management System

A production‑ready inventory management system with multi‑location stock, sales orders, customer management, audit logs, REST API, and barcode scanning.

## Features
- Multi‑location stock tracking
- Advanced user roles & permissions
- Sales orders & customer management
- Real‑time stock updates with audit logs
- Barcode/QR scanning (web)
- Interactive dashboards with charts
- CSV reports
- REST API for mobile integration
- Production security (HTTPS, rate limiting, etc.)
- CI with GitHub Actions

## Tech Stack
- Django 4.2, PostgreSQL
- Bootstrap 5, Chart.js
- Django REST Framework
- Simple‑History
- Sentry

## Installation
1. Clone the repository
2. Create virtual environment and install dependencies: `pip install -r requirements.txt`
3. Set environment variables (see `.env.example`)
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Run development server: `python manage.py runserver`

## Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md)

## API Documentation
When running, visit `/api/docs/` for Swagger UI.

## License
MIT