# Deployment Instructions

## Prerequisites
- Ubuntu 20.04 server (or similar)
- Python 3.10+, PostgreSQL, Nginx, Gunicorn

## Steps
1. Clone the repository on the server.
2. Install system dependencies: `sudo apt update && sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib`
3. Create a PostgreSQL database and user.
4. Set up environment variables in `.env`.
5. Install Python packages in a virtual environment.
6. Run migrations and collectstatic: `python manage.py migrate && python manage.py collectstatic --noinput`
7. Configure Gunicorn to run the app (create a systemd service).
8. Configure Nginx as a reverse proxy.
9. Enable HTTPS with Let's Encrypt.

See [Django deployment docs](https://docs.djangoproject.com/en/4.2/howto/deployment/) for details.