# 🚀 Job Application Tracker API

A **Job tracker backend API** built with **FastAPI** to help users track their job and internship applications efficiently.  
The system supports **secure authentication**, **user-specific data access**, and **CRUD operations** for job applications.

This project is designed with **clean architecture**, **JWT authentication**, and **scalable backend practices**, making it suitable for real-world usage and placement interviews.

---

## ✨ Features

- 🔐 User Registration & Login (JWT Authentication)
- 🧾 Create, Read job applications
- 👤 User-specific data isolation
- 🔒 Secure password hashing (bcrypt)
- ⚡ FastAPI with automatic Swagger documentation
- 🗄️ SQLAlchemy ORM
- 📦 Clean, modular, production-style codebase

---

## 🧰 Tech Stack

### Backend
- **FastAPI**
- **Python 3.10+**
- **SQLAlchemy**
- **SQLite** (can be replaced with PostgreSQL)
- **JWT (JSON Web Tokens)**

### Security
- Password hashing using **bcrypt**
- Token-based authentication

---

## 📂 Project Structure

│
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
│
├── requirements.txt
└── README.md

---


---

## 🔗 API Endpoints

### Authentication
| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login & get JWT token |

### Job Applications (Protected)
| Method | Endpoint | Description |
|------|---------|------------|
| POST | `/applications` | Add a job application |
| GET | `/applications` | Get all applications for logged-in user |

---

## 🔐 Authentication Flow

1. User logs in using `/auth/login`
2. Server returns a **JWT access token**
3. Client sends token in headers:
   ```http
   Authorization: Bearer <token>
4. Protected routes validate token and allow access
```
## ⚙️ Setup & Run Locally
1️⃣ Clone the repository
git clone https://github.com/your-username/job-tracker-backend.git
cd job-tracker-backend

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the server
uvicorn app.main:app --reload

📘 API Documentation

FastAPI provides automatic Swagger UI:

👉 http://127.0.0.1:8000/docs

🧪 Example Request (Create Application)
POST /applications
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```
```
{
  "company": "Google",
  "role": "Software Engineer",
  "status": "Applied"
}
```


## 🧠 What I Learned

- Building secure REST APIs with FastAPI

- JWT authentication & authorization

- Database modeling using SQLAlchemy

- Backend architecture best practices

- Frontend–backend integration readiness

## 📌 Future Enhancements

- Update & delete job applications

- Application status analytics

- Role-based access

- Email reminders

- Deployment with PostgreSQL