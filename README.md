# WildWheel Bike Rental & AI Assistant

WildWheel is a modern Django-based bike rental platform featuring a persistent AI assistant powered by **RAG (Retrieval-Augmented Generation)**. The application integrates real-time bike availability, online booking, and the ability to manage current reservations.

## 🚀 Key Features

* **AI Chat Assistant**: A global, persistent chat widget integrated across all pages with real-time Markdown rendering.
* **RAG Architecture**: Uses **OpenAI (GPT-4o)** and **pgvector** to answer queries based on custom Markdown documentation and bike inventory.
* **Smart Availability**: The AI follows strict business logic to recommend bike sizes based on user height and up-sell rental packages.
* **Bike Reservations**: Online bike booking system for a diverse fleet.
* **Social Auth**: Secure login via Google (using `django-allauth`).
* **Modern DevOps**: Fully containerized environment using Docker and high-performance dependency management.

## 🛠 Tech Stack

* **Backend**: Python 3.12+, Django 5.x
* **AI/ML**: OpenAI API (`gpt-4o`, `text-embedding-3-small`), `pgvector` for PostgreSQL
* **Database**: PostgreSQL with Vector storage enabled
* **Frontend**: Bootstrap 5, JavaScript (Async/Await Fetch API), Marked.js (Markdown rendering)
* **Environment**: Docker & Docker Compose

## 📦 Setup & Installation

### 1. Prerequisites
* Docker and Docker Compose installed.
* OpenAI API Key.

### 2. Configuration
Create a `.env` file in the root directory based on the following template:
```env
DEBUG=True
SECRET_KEY=your_django_secret_key
OPENAI_API_KEY=your_openai_api_key

# Database
DB_NAME=wildwheeldb
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Social Auth
GOOGLE_CLIENT_ID=your_id
```

### ▶️ Launching the App

The project is fully containerized.

To build images and start all services, run:

```bash
docker-compose up -d --build
```

Once all containers are running, the application will be available on:
```http://localhost:8000```

### Database Initialization
After starting the containers, apply migrations and create a superuser for the Django admin panel:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### AI Knowledge Management

The AI knowledge base is built from Markdown files located in:
```ai_bot/knowledge/```

- Sync Bike Fleet: Generate Markdown knowledge from the database.
```docker-compose exec web python manage.py update_bike_catalog```
- Reload Knowledge Base: Rebuild vector embeddings in pgvector.
```docker-compose exec web python manage.py update_knowledge```

### Testing
Run the full AI and backend test suite:
```docker-compose exec web pytest ai_bot/tests/```

### AI System Overview
The AI assistant uses a Retrieval-Augmented Generation pipeline:
1. User input is embedded into vector space
2. Relevant Markdown knowledge is retrieved using pgvector
3. Context is injected into the LLM prompt
4. The model generates a grounded response aligned with business rules

### License
MIT License
