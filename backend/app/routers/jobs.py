from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/")
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can post jobs")

    new_job = models.Job(**job.dict(), employer_id=user.id)
    db.add(new_job)
    db.commit()
    return {"message": "Job posted successfully"}

@router.get("/", response_model=list[schemas.JobOut])
def list_jobs(
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    location: str = "",
    db: Session = Depends(get_db)
):
    query = db.query(models.Job)
    if search:
        query = query.filter(models.Job.title.contains(search) | models.Job.description.contains(search))
    if location:
        query = query.filter(models.Job.location.contains(location))
    return query.offset(skip).limit(limit).all()

@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/employer/", response_model=list[schemas.JobOut])
def list_employer_jobs(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can view their jobs")
    return db.query(models.Job).filter(models.Job.employer_id == user.id).all()

@router.get("/{job_id}/applications")
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = db.query(models.Job).filter(models.Job.id == job_id, models.Job.employer_id == user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")

    applications = db.query(models.Application).filter(models.Application.job_id == job_id).all()
    return applications

@router.put("/{job_id}/applications/{app_id}")
def update_application_status(
    job_id: int,
    app_id: int,
    status: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = db.query(models.Job).filter(models.Job.id == job_id, models.Job.employer_id == user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")

    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.job_id == job_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    if status not in ["Applied", "Interview", "Rejected", "Offer"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    app.status = status
    db.commit()
    return {"message": "Application status updated"}