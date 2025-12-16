from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..deps import get_db
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = models.User(
        email=user.email,
        hashed_password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not db_user or not auth.verify_password(
        form_data.password, db_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
