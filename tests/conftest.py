"""Shared pytest fixtures for the test suite."""

from __future__ import annotations

from collections.abc import Generator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.router import api_router
from app.core.security import create_access_token, hash_password
from app.database.base import Base
from app.database.dependencies import get_db
from app.exceptions.handlers import register_exception_handlers
from app.models.user import User

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, Any, None]:
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_database() -> Generator[None, Any, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def app() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router)
    register_exception_handlers(application)
    application.dependency_overrides[get_db] = override_get_db
    return application


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session() -> Generator[Session, Any, None]:
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@pytest.fixture
def test_user(db_session: Session) -> User:
    user = User(
        full_name="Test User",
        email="test@example.com",
        password_hash=hash_password("TestPass123"),
        phone_number="+1234567890",
        role="user",
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def admin_user(db_session: Session) -> User:
    user = User(
        full_name="Admin User",
        email="admin@example.com",
        password_hash=hash_password("AdminPass123"),
        role="admin",
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def user_token(test_user: User) -> str:
    return create_access_token(
        user_id=test_user.id,
        email=test_user.email,
        role=test_user.role,
    )


@pytest.fixture
def admin_token(admin_user: User) -> str:
    return create_access_token(
        user_id=admin_user.id,
        email=admin_user.email,
        role=admin_user.role,
    )


@pytest.fixture
def auth_headers(user_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def admin_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}
