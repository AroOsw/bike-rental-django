# Bike Rental Django Project

## Introduction

A Django-based bike rental application allowing online bike reservations, consultant chat, and login via Google/Facebook.

## Features

- Online bike reservation system
- Google and Facebook login (using django-allauth)
- Real-time consultant chat
- Secure configuration with python-dotenv

## Technologies

- Python 3.10+
- Django
- Bootstrap (frontend)
- uv
- python-dotenv (environment variable management)
- Full dependency list in requirements.txt

## Setup Instructions

### Clone the repository:
git clone https://github.com/your-username/bike-rental-app.git
cd bike-rental-app

### Install dependencies:Ensure you have Python 3.10+ installed, then run:
pip install -r requirements.txt

### Configure environment variables:

Create a .env file in the project root based on example.env:

- DB_NAME=wildwheeldb
- DB_USER=your_database_user
- DB_PASSWORD=your_database_password
- DB_HOST=localhost
- DB_PORT=5432
- SECRET_KEY=your_secret_key
- DEBUG=True
- GOOGLE_CLIENT_ID=your_google_client_id
- FACEBOOK_APP_ID=your_facebook_app_id

- Update .env with your credentials (e.g., database URL, Google/Facebook API keys).


Apply database migrations:
python manage.py migrate


### Run the development server:

- python manage.py runserver
- Access the app at http://localhost:8000.


#### Notes

Ensure .env is not committed to Git (it’s ignored in .gitignore).
For production, set DEBUG=False and configure environment variables on your hosting platform (e.g., Heroku).

