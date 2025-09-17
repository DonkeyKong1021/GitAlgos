from typing import Optional

from sqlalchemy.orm import Session

from app.db import models
from app.utils.security import hash_password


def create_user(db: Session, email: str, password: str, role: models.UserRole) -> models.User:
    user = models.User(email=email.lower(), password_hash=hash_password(password), role=role.value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email.lower()).first()


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()
