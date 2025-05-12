📱 WhatsApp Messenger Backend API
FastAPI-based backend for a WhatsApp-style messenger. Supports user authentication, WhatsApp API integration via PyWa, background task management with Celery & Redis, and containerized deployment using Docker.

----------------------------


Features
🔐 User Authentication

Registration & login system

JWT token-based authentication

Secure password hashing

📲 WhatsApp Integration

PyWa library used to connect to WhatsApp Cloud API

Ready to send/receive messages via WhatsApp

⚙️ Background Tasks

Celery & Redis configured

Example task setup (can be extended to message delivery, logging, etc.)

🐳 Dockerized Setup

Dockerfile and docker-compose.yml included

Easy deployment with all services (FastAPI, Redis, etc.)

📘 API Docs

Automatic docs with Swagger UI and ReDoc (available at /docs and /redoc)


----------------------------


🛠️ Tech Stack
Python 3.11+

FastAPI

PostgreSQL

SQLAlchemy

JWT (via fastapi-jwt-auth)

PyWa (WhatsApp Cloud API Python wrapper)

Celery + Redis

Docker & Docker Compose


----------------------------


🧪 Example Endpoints
POST /register – register a user

POST /login – login and receive JWT token

POST /send-message – send WhatsApp message (requires auth)

GET /docs – Swagger docs

GET /redoc – ReDoc docs

