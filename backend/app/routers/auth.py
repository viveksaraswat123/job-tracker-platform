from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pathlib import Path
import jwt

from ..schemas import UserProfileOut, UserProfileUpdate, Token
from .. import models, auth
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
JWT_SECRET = "MY_SECRET_KEY_BKL"

def get_db_user(uid: int, db: Session):
    user = db.query(models.User).filter(models.User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.username).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email=user.username,
        hashed_password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email, "message": "User registered successfully"}

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserProfileOut)
def me(user=Depends(get_current_user)):
    return user

@router.get("/profile", response_model=UserProfileOut)
def full_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return get_db_user(user.id, db)

@router.put("/profile/update")
def update_profile(data: UserProfileUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = get_db_user(user.id, db)

    for key, value in data.dict().items():
        if value is not None:
            setattr(db_user, key, value)

    db.commit()
    return {"message": "Profile updated successfully"}

@router.post("/profile/avatar")
def upload_avatar(file: UploadFile = File(...), user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = get_db_user(user.id, db)

    save_dir = Path("frontend/static/avatars")
    save_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{db_user.id}-{file.filename}"
    file_path = save_dir / filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    db_user.avatar = f"/static/avatars/{filename}"
    db.commit()
    return {"message": "Avatar uploaded successfully"}

@router.post("/profile/resume")
def upload_resume(file: UploadFile = File(...), user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = get_db_user(user.id, db)

    save_dir = Path("frontend/static/resume")
    save_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{db_user.id}-{file.filename}"
    file_path = save_dir / filename
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    db_user.resume = f"/static/resume/{filename}"
    db.commit()
    return {"message": "Resume uploaded successfully"}

@router.get("/profile/stats")
def profile_stats(user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = get_db_user(user.id, db)
    apps = db.query(models.Application).filter(models.Application.owner_id == db_user.id).all()

    return {
        "applied": len([a for a in apps if a.status == "Applied"]),
        "interview": len([a for a in apps if a.status == "Interview"]),
        "rejected": len([a for a in apps if a.status == "Rejected"]),
        "offers": len([a for a in apps if a.status == "Offer"])
    }

@router.get("/profile/timeline")
def profile_timeline(user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = get_db_user(user.id, db)
    apps = db.query(models.Application).filter(models.Application.owner_id == db_user.id).all()
    return [f"{a.company} → {a.status} ({a.date})" for a in apps]
