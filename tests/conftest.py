import os
from typing import Generator

from cryptography.fernet import Fernet
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("FERNET_SECRET", Fernet.generate_key().decode())
os.environ.setdefault("SECRET_KEY_BASE", "testsecret")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("ALPHA_VANTAGE_API_KEY", "demo")

from app.main import app
from app.db.base import Base
from app.db.session import get_db

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
