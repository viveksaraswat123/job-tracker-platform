from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth, applications

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Tracker API")

app.include_router(auth.router)
app.include_router(applications.router)

@app.get("/")
def health():
    return {"status": "API running"}
