from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from sqlalchemy.orm import Session
from .database import engine
from . import models
from .routers import auth, applications, add_page
from .deps import get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(add_page.router)  # 👈 mounted add page

frontend_path = Path(__file__).parent.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

@app.get("/")
def serve_homepage():
    return FileResponse(frontend_path / "index.html")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse(frontend_path / "dashboard.html")

@app.get("/profile")
def serve_profile_page():
    return FileResponse(frontend_path / "profile.html")

@app.get("/health")
def health():
    return {"status": "API running"}
