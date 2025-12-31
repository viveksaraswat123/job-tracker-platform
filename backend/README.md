# 🚀 Job Application Tracker API

A robust and modern backend API built with **FastAPI** to help students, fresh graduates, and professionals **track, organize, and manage job & internship applications** in one place.

Designed with **industry-grade architecture**, **JWT authentication**, and **scalable backend principles**, this API enables users to isolate and control their own application data securely — making it a perfect foundation for real-world products and placement interviews.

---

## ✨ Key Capabilities

- 🔐 **Secure user authentication** (Register/Login via JWT)
- 🧾 **Create and manage job applications** (CRUD support)
- 👤 **User-specific data isolation** for privacy and security
- 🔒 **Password hashing using bcrypt (bcrypt)** — no plain password stored
- 🗄️ **SQLAlchemy ORM** for clean database modeling
- ⚡ **Auto-generated API documentation** using FastAPI (Swagger UI)
- 📦 **Modular & maintainable codebase** for easy scaling
- 🎯 **Production-ready backend practices** applied from day one

---

## 🧰 Technology Stack

### Backend Core
- **FastAPI**
- **Python 3.10+**
- **SQLAlchemy ORM**
- **SQLite (Development DB)** → can be replaced with PostgreSQL

### Security & Authentication
- **bcrypt** for password hashing
- **JWT (JSON Web Token)** for authorization
- **OAuth2PasswordBearer** for protected route access

---

## 📂 Clean Project Layout

├── app/
│ ├── main.py
│ ├── config.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── auth.py
│ ├── deps.py
│ └── routers/
│ ├── auth.py
│ └── applications.py
├── requirements.txt
└── README.md


This structure keeps every module **decoupled, reusable, testable, and developer-friendly**, exactly like a real product backend should be.

---

## 🔗 Available API Routes

### Authentication (Public)
| Method | Route | Description |
|--------|--------|-------------|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Authenticate and receive a JWT token |

### Applications (Protected)
| Method | Route | Description |
|--------|--------|-------------|
| POST | `/applications` | Add a new job/internship application |
| GET | `/applications` | Fetch all applications for the logged-in user |
| GET | `/applications/{id}` | Get a single application detail |
| PUT | `/applications/{id}` | Update an existing application |
| DELETE | `/applications/{id}` | Remove an application |

Each protected route validates the token automatically and ensures **only the owner can access or modify their own data**.

---

## 🔐 How Authentication Works

1. User logs in via `/auth/login`
2. Server returns a signed **JWT token**
3. Client stores and sends it in headers like:


4. Backend extracts user ID from token and grants access only if valid
5. All sensitive routes ensure **data isolation by owner**

This flow mimics **exact real-world API security standards** used in platforms like Indeed, Naukri, LinkedIn, etc.

---

## ⚙️ Local Setup & Run Guide

```bash
git clone https://github.com/your-username/job-tracker-backend.git
cd job-tracker-backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
