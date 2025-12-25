from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/")
def create_application(
    app: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_app = models.Application(**app.dict(), owner_id=user.id)
    db.add(new_app)
    db.commit()
    return {"message": "Application added"}

@router.get("/", response_model=list[schemas.ApplicationOut])
def list_applications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(models.Application).filter(
        models.Application.owner_id == user.id
    ).all()

@router.get("/{app_id}", response_model=schemas.ApplicationOut)
def get_application(
    app_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    app = db.query(models.Application).filter(
        models.Application.id == app_id,
        models.Application.owner_id == user.id
    ).first()

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    return app

@router.put("/{app_id}")
def update_application(
    app_id: int,
    app_data: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    app = db.query(models.Application).filter(
        models.Application.id == app_id,
        models.Application.owner_id == user.id
    ).first()

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.company = app_data.company
    app.role = app_data.role
    app.status = app_data.status

    db.commit()
    return {"message": "Application updated"}

@router.delete("/{app_id}")
def delete_application(
    app_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    app = db.query(models.Application).filter(
        models.Application.id == app_id,
        models.Application.owner_id == user.id
    ).first()

    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(app)
    db.commit()
    return {"message": "Application deleted"}
