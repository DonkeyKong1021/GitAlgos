from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import schemas
from app.auth.service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    persist_refresh_token,
    rotate_refresh_token,
)
from app.deps import get_current_user
from app.db import models
from app.db.crud import users as users_crud
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = users_crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User exists")
    try:
        role = models.UserRole(payload.role)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid role") from exc
    user = users_crud.create_user(db, payload.email, payload.password, role)
    return user


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    persist_refresh_token(db, user.id, refresh)
    return schemas.Token(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=schemas.Token)
def refresh(payload: schemas.RefreshRequest, db: Session = Depends(get_db)):
    record = rotate_refresh_token(db, payload.refresh_token)
    access = create_access_token(str(record.user_id))
    return schemas.Token(access_token=access, refresh_token=record.token)


@router.get("/me", response_model=schemas.UserRead)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
