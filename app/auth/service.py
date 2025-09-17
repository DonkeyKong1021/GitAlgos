from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db import models
from app.db.crud import users as users_crud
from app.settings import settings
from app.utils.security import verify_password

ALGORITHM = "HS256"


def _create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {"sub": str(subject), "iat": now, "exp": now + expires_delta, "type": token_type}
    return jwt.encode(payload, settings.secret_key_base, algorithm=ALGORITHM)


def create_access_token(subject: str) -> str:
    return _create_token(subject, timedelta(minutes=settings.access_token_expire_minutes), "access")


def create_refresh_token(subject: str) -> str:
    return _create_token(subject, timedelta(minutes=settings.refresh_token_expire_minutes), "refresh")


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key_base, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    return payload


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    user = users_crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return user


def persist_refresh_token(db: Session, user_id: int, token: str) -> models.RefreshToken:
    now = datetime.now(tz=timezone.utc)
    expires_at = now + timedelta(minutes=settings.refresh_token_expire_minutes)
    rt = models.RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt


def rotate_refresh_token(db: Session, old_token: str) -> models.RefreshToken:
    record = (
        db.query(models.RefreshToken)
        .filter(models.RefreshToken.token == old_token, models.RefreshToken.revoked.is_(False))
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    if record.expires_at < datetime.now(tz=timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired refresh token")
    record.revoked = True
    db.add(record)
    db.commit()
    db.refresh(record)
    new_token = create_refresh_token(str(record.user_id))
    return persist_refresh_token(db, record.user_id, new_token)
