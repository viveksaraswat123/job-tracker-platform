from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import UploadFile, File
from pathlib import Path
from ..schemas import UserProfileOut, UserProfileUpdate
from .. import schemas, models, auth
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = models.User(
        email=user.email,
        hashed_password=auth.hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "message": "User registered successfully"
    }


@router.post(
    "/login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    # Constant-time style check (cleaner auth logic)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not auth.verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = auth.create_access_token(
        {"sub": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.UserOut)
def get_current_user_info(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return user


# GET full profile
@router.get("/profile", response_model=UserProfileOut)
def full_profile(user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    return db_user


# UPDATE profile details
@router.put("/profile/update")
def update_profile(
    profile: UserProfileUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()

    for key, value in profile.dict().items():
        if value is not None:
            setattr(db_user, key, value)

    db.commit()
    return {"message": "Profile updated successfully"}


# UPLOAD avatar
@router.post("/profile/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    save_path = Path("frontend/static/avatars")
    save_path.mkdir(parents=True, exist_ok=True)

    filename = f"{user.id}-{file.filename}"
    with open(save_path / filename, "wb") as f:
        f.write(file.file.read())

    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    db_user.avatar = f"/static/avatars/{filename}"
    db.commit()

    return {"message": "Avatar uploaded successfully"}


# UPLOAD resume
@router.post("/profile/resume")
def upload_resume(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    save_path = Path("frontend/static/resume")
    save_path.mkdir(parents=True, exist_ok=True)

    filename = f"{user.id}-{file.filename}"
    with open(save_path / filename, "wb") as f:
        f.write(file.file.read())

    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    db_user.resume = f"/static/resume/{filename}"
    db.commit()

    return {"message": "Resume uploaded successfully"}


# PROFILE ANALYTICS
@router.get("/profile/stats")
def profile_stats(user=Depends(get_current_user), db: Session = Depends(get_db)):
    apps = db.query(models.Application).filter(models.Application.user_id == user.id).all()

    return {
        "applied": len([a for a in apps if a.status=="Applied"]),
        "interview": len([a for a in apps if a.status=="Interview"]),
        "rejected": len([a for a in apps if a.status=="Rejected"]),
        "offers": len([a for a in apps if a.status=="Offer"])
    }


# PROFILE TIMELINE
@router.get("/profile/timeline")
def profile_timeline(user=Depends(get_current_user), db: Session = Depends(get_db)):
    apps = db.query(models.Application).filter(models.Application.user_id == user.id).all()
    return [f"{a.company} → {a.status} ({a.date})" for a in apps]
