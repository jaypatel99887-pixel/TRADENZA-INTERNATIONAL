"""
Tradenza International Private Limited - Production WSGI Entry Point
For deployment with Gunicorn, uWSGI, Waitress, or Apache mod_wsgi.

Usage:
    gunicorn wsgi:app
    waitress-serve --port=5000 wsgi:app
"""

from app import app

if __name__ == "__main__":
    app.run()
