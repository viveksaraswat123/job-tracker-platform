# Job Application Tracker API

This is a backend API built with FastAPI for tracking and managing job and internship applications. It provides secure user authentication and data isolation, making it suitable for personal or professional use.

## Features

- User registration and login with JWT authentication
- CRUD operations for job applications
- Secure password hashing with bcrypt
- Database integration using SQLAlchemy ORM
- Auto-generated API documentation via FastAPI
- Modular codebase for easy maintenance and scaling

## Technology Stack

### Backend
- FastAPI
- Python 3.10+
- SQLAlchemy ORM
- SQLite (for development; can be switched to PostgreSQL)

### Security
- bcrypt for password hashing
- JWT for token-based authentication
- OAuth2 for protected routes

## Project Structure

`
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── deps.py
│   └── routers/
│       ├── auth.py
│       └── applications.py
├── requirements.txt
└── README.md
`

## API Endpoints

### Authentication
- POST /auth/register - Register a new user
- POST /auth/login - Login and obtain JWT token

### Applications (requires authentication)
- POST /applications - Create a new application
- GET /applications - List all applications for the user
- GET /applications/{id} - Get details of a specific application
- PUT /applications/{id} - Update an application
- DELETE /applications/{id} - Delete an application

## Authentication Flow

1. Register or login to receive a JWT token.
2. Include the token in the Authorization header for protected requests: Authorization: Bearer <token>
3. The API validates the token and ensures users can only access their own data.

## Setup and Installation

1. Clone the repository:
   `
   git clone https://github.com/your-username/job-tracker-backend.git
   cd job-tracker-backend
   `

2. Create a virtual environment:
   `
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   `

3. Install dependencies:
   `
   pip install -r requirements.txt
   `

4. Run the application:
   `
   uvicorn app.main:app --reload
   `

The API will be available at http://localhost:8000, with documentation at http://localhost:8000/docs.
