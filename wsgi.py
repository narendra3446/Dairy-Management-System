"""
WSGI entry point for production deployment
Used by Gunicorn, Heroku, Railway, Render, and other deployment platforms
"""
import os
from app_complete import app

if __name__ == "__main__":
    app.run()