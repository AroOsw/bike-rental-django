#Bike Rental Django Project

##Introduction

A web application for bike rentals, built with Django to showcase full-stack development skills. Features include bike browsing, online reservations, real-time chat, and Google/Facebook login. This project is versioned on GitHub for portfolio purposes.

##Technologies Backend: Python 3.13, Django 5.2.3 Frontend: Bootstrap 5 Database: PostgreSQL Package Management: uv Dependencies: psycopg2-binary, pillow, python-decouple, django-channels, social-auth-app-django

##Setup Instructions

Clone the repository:

git clone https://github.com/YOUR_USERNAME/bike-rental-django.git cd bike-rental-django

Install uv: pip install uv

Install Python 3.13: uv python install 3.13 --preview

Create and activate virtual environment: uv venv --python 3.13 source .venv/bin/activate # Linux/macOS ..venv\Scripts\activate # Windows

Install dependencies: uv pip install -r requirements.txt

Configure PostgreSQL: Create a database named bike_rental_db.

Add .env file with: DATABASE_URL=postgresql://postgres:your_password@localhost:5432/bike_rental_db SECRET_KEY=your_django_secret_key

Apply migrations: python manage.py migrate

Run the server: python manage.py runserver

Open http://localhost:8000 to view the app.