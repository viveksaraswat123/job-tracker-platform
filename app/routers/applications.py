from fastapi import APIRouter, Depends
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
