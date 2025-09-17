from typing import List, Optional

from sqlalchemy.orm import Session

from app.db import models


def create_credential(
    db: Session,
    *,
    owner_id: int,
    broker: models.BrokerType,
    key_id: str,
    secret_encrypted: bytes,
    paper: bool,
) -> models.ApiCredential:
    cred = models.ApiCredential(
        owner_id=owner_id,
        broker=broker,
        key_id=key_id,
        secret_encrypted=secret_encrypted,
        paper=paper,
    )
    db.add(cred)
    db.commit()
    db.refresh(cred)
    return cred


def list_credentials(db: Session, owner_id: int) -> List[models.ApiCredential]:
    return db.query(models.ApiCredential).filter(models.ApiCredential.owner_id == owner_id).all()


def get_credential(db: Session, credential_id: int, owner_id: int) -> Optional[models.ApiCredential]:
    return (
        db.query(models.ApiCredential)
        .filter(models.ApiCredential.id == credential_id, models.ApiCredential.owner_id == owner_id)
        .first()
    )
